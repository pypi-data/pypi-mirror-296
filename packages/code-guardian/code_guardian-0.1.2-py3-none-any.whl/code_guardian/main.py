import concurrent.futures
import inspect
import os
import re
import subprocess
import time
from typing import Any, List

from loguru import logger
from pydantic import BaseModel, Field
from swarms import Agent

from code_guardian.prompt import TEST_WRITER_SOP_PROMPT
from swarms.structs.concat import concat_strings


# Pydantic model for metadata
class TestResult(BaseModel):
    class_name: str
    class_docstring: str
    class_source_code: str
    test_file_path: str
    test_file_content: str
    status: str  # "success" or "failure"
    message: str  # Detailed message


class CodeGuardianLog(BaseModel):
    tests: List[TestResult]
    timestamp: str = Field(
        time.strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of the log",
    )


class CodeGuardian:
    """
    Initialize CodeGuardian with the provided classes, agent, and directory path.

    Args:
        classes (List[Any]): A list of classes for which tests will be generated.
        agent (OpenAIChat): The agent responsible for generating tests using the OpenAIChat model.
        dir_path (str): The directory where generated tests will be saved. Defaults to "tests/memory".
    """

    def __init__(
        self,
        classes: List[Any],
        agent: Agent = None,
        dir_path: str = "tests/memory",
        package_name: str = "swarms",
        module_name: str = "swarms.memory",
    ):
        self.classes = classes
        self.agent = agent
        self.dir_path = dir_path
        self.package_name = package_name
        self.module_name = module_name
        # self.test_results: List[TestResult] = []

        # Set up the logger
        logger.add(
            "code_guardian.log",
            format="{time} {level} {message}",
            level="DEBUG",
        )
        logger.info("CodeGuardian initialized.")

        # Log
        self.log = CodeGuardianLog(
            tests=[],
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def extract_code_from_markdown(
        self, markdown_content: str
    ) -> str:
        """
        Extracts code blocks from a Markdown string and returns them as a single string.

        Args:
            markdown_content (str): The Markdown content as a string.

        Returns:
            str: A single string containing all the code blocks separated by newlines.
        """
        pattern = r"```(?:\w+\n)?(.*?)```"
        matches = re.findall(pattern, markdown_content, re.DOTALL)
        return "\n".join(code.strip() for code in matches)

    def create_test(self, cls: Any):
        """
        Processes the class's docstring and source code to create test files and runs them until successful.

        Args:
            cls (Any): The class to generate tests for.
        """
        class_name = cls.__name__
        logger.debug(
            f"Starting test generation for class: {class_name}"
        )

        # Retrieve class documentation and source code
        doc, source = self.get_class_details(cls)
        input_content = self.prepare_input_content(
            class_name, doc, source
        )
        prompt = TEST_WRITER_SOP_PROMPT(
            input_content, self.package_name, self.module_name
        )

        # Initialize result list for context tracking
        results = [prompt]

        try:
            while True:  # Keep running until the test passes
                logger.debug(
                    f"Generating test code for class {class_name}"
                )

                # Generate test code using agent
                test_code = self.generate_test_code(prompt)
                results.append(test_code)

                # Create and write the test file
                file_path = self.write_test_file(
                    class_name, test_code
                )

                # Run the test
                test_output = self.run_test_file(file_path)
                results.append(test_output)

                if (
                    "failed" not in test_output
                ):  # Break the loop if the test is successful
                    logger.info(
                        f"Test for {class_name} passed successfully."
                    )
                    self.log_test_success(
                        class_name, doc, source, file_path, test_code
                    )
                    break
                else:
                    # If the test failed, append context and retry
                    logger.warning(
                        f"Test for {class_name} failed. Retrying with updated context."
                    )
                    prompt = self.concat_results_for_retry(results)

        except Exception as e:
            logger.error(
                f"Error while creating test for class {class_name}: {e}"
            )

    def generate_tests(self):
        """
        Generates test files for all classes in a multi-threaded manner.
        """
        logger.info("Starting test generation for all classes.")

        with concurrent.futures.ThreadPoolExecutor() as executor:  # Use ThreadPoolExecutor for concurrent execution
            # Submit each class to the executor individually
            futures = {
                executor.submit(self.create_test, cls): cls
                for cls in self.classes
            }
            for future in concurrent.futures.as_completed(
                futures
            ):  # Wait for each future to complete
                cls = futures[
                    future
                ]  # Get the class associated with the future
                try:
                    future.result()  # Retrieve the result (or raise exception if occurred)
                except Exception as e:
                    logger.error(
                        f"Error generating test for class {cls}: {e}"
                    )

        # Log
        logger.info("Test generation finished")

    def run_all_tests(
        self, return_json: bool = False
    ) -> List[TestResult]:
        """
        Runs all tests using subprocess and records the results.

        Args:
            return_json (bool): Whether to return results in JSON format.

        Returns:
            List[TestResult]: A list of test results (success or failure).
        """
        test_files = os.listdir(self.dir_path)
        logger.info(f"Running tests from directory: {self.dir_path}")

        for test_file in test_files:
            if test_file.endswith(".py"):
                try:
                    # Run the test file using subprocess
                    result = subprocess.run(
                        [
                            "python",
                            os.path.join(self.dir_path, test_file),
                        ],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    self.test_results.append(
                        TestResult(
                            class_name=test_file,
                            status="success",
                            message=result.stdout,
                        )
                    )
                    logger.info(f"Test {test_file} passed.")
                except subprocess.CalledProcessError as e:
                    self.test_results.append(
                        TestResult(
                            class_name=test_file,
                            status="failure",
                            message=e.stderr,
                        )
                    )
                    logger.error(
                        f"Test {test_file} failed with error: {e.stderr}"
                    )

        if return_json:
            return [result.json() for result in self.test_results]
        return self.test_results

    def check_tests_results(self, return_json: bool = False):
        """
        Main method to generate and run all tests.

        Args:
            return_json (bool): Whether to return results in JSON format.
        """
        logger.info("Starting test generation and execution.")
        self.generate_tests()
        results = self.run_all_tests(return_json=return_json)
        if return_json:
            logger.info("Returning results in JSON format.")
            print(results)
        else:
            for result in results:
                logger.info(
                    f"{result.class_name} - {result.status}: {result.message}"
                )
                print(
                    f"{result.class_name} - {result.status}: {result.message}"
                )

    def check_successful(self, content: str):
        if "successfully" in content:
            return "The test ran successfully"

    def run_test_file(self, file_name: str):
        """
        Runs a specified test file using subprocess.

        Args:
            file_name (str): The name of the test file to run.
        """
        file_path = os.path.join(
            self.dir_path, file_name
        )  # Construct the full file path
        try:
            # Run the test file using subprocess
            result = subprocess.run(
                ["python3", file_path],
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info(
                f"Test {file_name} ran successfully with output:\n{result.stdout}"
            )
            prompt = f"Test {file_name} ran successfully with output:\n{result.stdout}"
            return prompt
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Test {file_name} failed with error:\n{e.stderr}"
            )
            # return e.stderr  # Return the error message
            prompt = (
                f"Test {file_name} failed with error:\n{e.stderr}"
            )
            return prompt

    def run(self, return_json: bool = False):
        """
        Main method to generate and run all tests.

        Args:
            return_json (bool): Whether to return results in JSON format.
        """
        logger.info("Creating tests now for input classes:")
        self.generate_tests()
        logger.info("Test generation finished.")

        return self.log.model_dump_json(indent=2)

    def get_class_details(self, cls: Any):
        """Retrieves the class docstring and source code."""
        doc = inspect.getdoc(cls)
        source = inspect.getsource(cls)
        return doc, source

    def prepare_input_content(
        self, class_name: str, doc: str, source: str
    ) -> str:
        """Prepares the input content for the agent based on class details."""
        return f"Class Name: {class_name}\n\nDocumentation:\n{doc}\n\nSource Code:\n{source}"

    def generate_test_code(self, prompt: str) -> str:
        """Generates the test code by running the agent with the provided prompt."""
        processed_content = self.agent.run(prompt)
        return self.extract_code_from_markdown(processed_content)

    def write_test_file(self, class_name: str, test_code: str) -> str:
        """Writes the generated test code to a file."""
        os.makedirs(self.dir_path, exist_ok=True)
        file_path_name = f"test_{class_name.lower()}.py"
        file_path = os.path.join(self.dir_path, file_path_name)

        with open(file_path, "w") as file:
            file.write(f"# {class_name}\n\n{test_code}\n")

        logger.debug(f"Test file written to: {file_path}")
        return file_path

    def concat_results_for_retry(self, results: list) -> str:
        """Concatenates all result strings into a single prompt for retry attempts."""
        return "\n".join(results)

    def log_test_success(
        self,
        class_name: str,
        doc: str,
        source: str,
        file_path: str,
        test_code: str,
    ):
        """Logs the successful test generation."""
        self.log.tests.append(
            TestResult(
                class_name=class_name,
                class_docstring=doc,
                class_source_code=source,
                test_file_path=file_path,
                test_file_content=test_code,
                status="success",
                message="Test file created and passed successfully",
            )
        )
        logger.info(
            f"Test result for {class_name} logged successfully."
        )
