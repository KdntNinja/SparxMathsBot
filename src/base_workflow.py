"""Base workflow class for SparxMathsBot."""

import io
import os
import logging
from time import sleep
from typing import Callable

from dotenv import load_dotenv
from PIL import Image
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .browser_manager import BrowserManager
from .config import SCHOOL_URL, USERNAME_ID, PASSWORD_ID, HOMEWORK_TEXT_CLASS_NAME
from .email_notifier import EmailNotifier
from .image_processor import ImageProcessor
from .logging_utils import log_function_call

load_dotenv()


class BaseSparxWorkflow:
    """Base workflow class for SparxMaths automation."""

    def __init__(self):
        """Initialize the base workflow with common components."""
        self.logger = logging.getLogger("SparxWorkflow")
        self.logger.debug("Initializing BaseSparxWorkflow...")

        # Initialize components
        self.browser = BrowserManager(headless=True)
        self.image_processor = ImageProcessor(use_gpu=True)
        self.email_notifier = EmailNotifier()

        # Load configuration from environment
        self._load_config()

        self.logger.debug("Base workflow components initialized.")

    def _load_config(self):
        """Load configuration from environment variables."""
        self.school_text = os.getenv("SCHOOL_TEXT")
        self.school_input_class_name = os.getenv("SCHOOL_INPUT_CLASS_NAME")
        self.username_text = os.getenv("USERNAME")
        self.password_text = os.getenv("PASSWORD")

    @log_function_call
    def run_workflow(self) -> None:
        """Execute the complete workflow."""
        self.logger.info("Running workflow...")
        self.browser.fullscreen()
        try:
            self.select_school()
            self.login()
            self.navigate_to_section()
            self.solve_questions()
            sleep(3)
        except Exception as e:
            self.logger.error(
                f"An error occurred during the workflow: {e}", exc_info=True
            )
        finally:
            self.cleanup()
            self.logger.info("Workflow run completed, cleanup executed.")

    @log_function_call
    def execute_step(self, step_func: Callable) -> None:
        """Execute a workflow step with error handling."""
        try:
            step_func()
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Error in {step_func.__name__}: {e}", exc_info=True)

    @log_function_call
    def select_school(self) -> None:
        """Navigate to school selection page and select school."""
        self.logger.debug(f"Opening school URL: {SCHOOL_URL}")
        self.browser.driver.get(SCHOOL_URL)

        input_element = self.browser.wait_for_element(
            By.CLASS_NAME, self.school_input_class_name
        )
        input_element.send_keys(self.school_text + Keys.RETURN)

        continue_button = self.browser.wait_for_element(
            By.XPATH, "//button[text()='Continue']", clickable=True
        )
        continue_button.click()
        self.logger.info("School selection complete.")

    @log_function_call
    def login(self) -> None:
        """Perform login with credentials."""
        self.browser.wait_for_element(By.ID, USERNAME_ID).send_keys(self.username_text)
        self.browser.wait_for_element(By.ID, PASSWORD_ID).send_keys(
            self.password_text + Keys.RETURN
        )
        self.logger.debug("Login attempted.")

    def navigate_to_section(self) -> None:
        """Navigate to specific section - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement navigate_to_section()")

    def solve_questions(self) -> None:
        """Solve questions - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement solve_questions()")

    def _click_canvas_location(self, location: tuple) -> None:
        """Click on canvas at specified coordinates."""
        canvas = self.browser.driver.find_element(By.TAG_NAME, "canvas")
        actions = ActionChains(self.browser.driver)
        x_offset, y_offset = location
        actions.move_to_element_with_offset(
            canvas, x_offset, y_offset
        ).click().perform()

    @log_function_call
    def cleanup(self) -> None:
        """Clean up resources and send completion notification."""
        try:
            self.browser.quit()
            self.logger.info("Web driver closed.")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}", exc_info=True)
        finally:
            self.email_notifier.send_completion_notification()
            self.logger.info("Email sent.")
