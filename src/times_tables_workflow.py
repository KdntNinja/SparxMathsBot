"""Times Tables workflow class for SparxMathsBot."""

import io
from random import uniform
from time import sleep

from PIL import Image
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base_workflow import BaseSparxWorkflow
from .config import (
    HOMEWORK_TEXT_CLASS_NAME,
    TIMES_TABLES_TEXT_XPATH,
    CLUB_CHECK_TEXT_XPATH,
    START_BUTTON_LOCATION,
    CROPPED_IMAGE_BOX,
    MAX_ATTEMPTS,
    INTERMEDIATE_CHECKPOINTS,
    TIMES_TABLES_EXIT_XPATH,
)
from .logging_utils import log_function_call


class TimesTablesWorkflow(BaseSparxWorkflow):
    """Workflow class specifically for SparxMaths Times Tables automation."""

    def __init__(self):
        """Initialize the Times Tables workflow."""
        super().__init__()
        self.logger.debug("TimesTablesWorkflow initialized.")

    @log_function_call
    def navigate_to_section(self) -> None:
        """Navigate to Times Tables section."""
        self.browser.wait_for_element(
            By.CLASS_NAME, HOMEWORK_TEXT_CLASS_NAME, clickable=True
        ).click()

        self.browser.wait_for_element(
            By.XPATH, TIMES_TABLES_TEXT_XPATH, clickable=True
        ).click()

        self.browser.wait_for_element(
            By.XPATH, CLUB_CHECK_TEXT_XPATH, clickable=True
        ).click()

        sleep(10)
        self.logger.info("Successfully navigated to Times Tables.")

    @log_function_call
    def solve_questions(self) -> None:
        """Solve the times tables quiz using OCR."""
        self.click_start_quiz()
        self.solve_quiz()

    @log_function_call
    def click_start_quiz(self) -> None:
        """Find and click the start quiz button using OCR."""
        text_to_find = "Start quiz"
        self.logger.debug("Entering loop to find and click start quiz button.")

        while True:
            screenshot = self.browser.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            extracted_text = self.image_processor.extract_text_pytesseract(image)

            if text_to_find in extracted_text:
                self.logger.debug("Start quiz button found. Proceeding to click it.")
                self._click_canvas_location(START_BUTTON_LOCATION)
                break

        self.logger.info("Successfully clicked start quiz button.")

    @log_function_call
    def solve_quiz(self) -> None:
        """Solve the times tables quiz using OCR."""
        successful_attempts = 0

        while successful_attempts < MAX_ATTEMPTS:
            screenshot = self.browser.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            cropped_image = self.image_processor.crop_image(image, CROPPED_IMAGE_BOX)

            # Convert to bytes for EasyOCR
            cropped_image_bytes = self.image_processor.image_to_bytes(cropped_image)
            extracted_text = self.image_processor.extract_text_easyocr(
                cropped_image_bytes
            )

            # Find multiplication problem
            problem = self.image_processor.find_multiplication_problem(extracted_text)

            # Periodic click to keep quiz active
            if successful_attempts % 10 == 0:
                self._click_canvas_location(START_BUTTON_LOCATION)

            if problem:
                num1, num2 = problem
                result = num1 * num2

                sleep(uniform(2, 3.5))

                self.browser.driver.find_element(By.TAG_NAME, "body").send_keys(
                    str(result) + Keys.RETURN
                )
                successful_attempts += 1

                # Handle checkpoints
                if successful_attempts in INTERMEDIATE_CHECKPOINTS:
                    self._handle_checkpoint()

    def _handle_checkpoint(self) -> None:
        """Handle intermediate checkpoints in the quiz."""
        self.browser.wait_for_element(
            By.XPATH, TIMES_TABLES_EXIT_XPATH, clickable=True
        ).click()

        self.browser.wait_for_element(
            By.XPATH, CLUB_CHECK_TEXT_XPATH, clickable=True
        ).click()

        self.click_start_quiz()


# For backward compatibility
SparxTTWorkflow = TimesTablesWorkflow
