"""General questions workflow class for SparxMathsBot."""

import io
import re
from random import uniform
from time import sleep
from typing import Dict, Any

from PIL import Image
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base_workflow import BaseSparxWorkflow
from .config import (
    HOMEWORK_TEXT_CLASS_NAME,
    START_BUTTON_LOCATION,
    CROPPED_IMAGE_BOX,
)
from .logging_utils import log_function_call


class GeneralQuestionsWorkflow(BaseSparxWorkflow):
    """Workflow class for general SparxMaths questions (algebra, geometry, etc.)."""

    def __init__(self):
        """Initialize the General Questions workflow."""
        super().__init__()
        self.logger.debug("GeneralQuestionsWorkflow initialized.")

        # Question patterns for different types
        self.question_patterns = {
            "addition": re.compile(r"(\d+)\s*\+\s*(\d+)\s*=\s*\?"),
            "subtraction": re.compile(r"(\d+)\s*-\s*(\d+)\s*=\s*\?"),
            "multiplication": re.compile(r"(\d+)\s*\*\s*(\d+)\s*=\s*\?"),
            "division": re.compile(r"(\d+)\s*÷\s*(\d+)\s*=\s*\?"),
            "simple_equation": re.compile(r"(\w+)\s*=\s*(\d+)"),
        }

    @log_function_call
    def navigate_to_section(self) -> None:
        """Navigate to homework/questions section."""
        self.browser.wait_for_element(
            By.CLASS_NAME, HOMEWORK_TEXT_CLASS_NAME, clickable=True
        ).click()

        # Look for available tasks/homework
        tasks = self.browser.driver.find_elements(
            By.XPATH, "//a[contains(@class, 'task') or contains(@class, 'homework')]"
        )

        if tasks:
            tasks[0].click()  # Click the first available task
            sleep(3)
            self.logger.info("Successfully navigated to homework section.")
        else:
            self.logger.warning("No homework tasks found.")

    @log_function_call
    def solve_questions(self) -> None:
        """Solve general math questions using OCR and pattern recognition."""
        self.start_question_solving()

    @log_function_call
    def start_question_solving(self) -> None:
        """Start solving questions with automatic detection."""
        questions_solved = 0
        max_questions = 50  # Configurable limit

        while questions_solved < max_questions:
            screenshot = self.browser.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))

            # Check if we can start a question
            if self._check_for_start_button(image):
                self._click_canvas_location(START_BUTTON_LOCATION)
                sleep(2)

            # Try to solve current question
            if self._solve_current_question(image):
                questions_solved += 1
                self.logger.info(f"Question {questions_solved} solved successfully.")
                sleep(uniform(2, 4))  # Random delay between questions
            else:
                # If we can't solve, try to skip or get hint
                self._handle_unsolved_question()

            # Check if we've completed all questions
            if self._check_completion(image):
                self.logger.info("All questions completed!")
                break

    def _check_for_start_button(self, image: Image.Image) -> bool:
        """Check if there's a start button visible."""
        text = self.image_processor.extract_text_pytesseract(image)
        return any(phrase in text.lower() for phrase in ["start", "begin", "continue"])

    def _solve_current_question(self, image: Image.Image) -> bool:
        """Attempt to solve the current question."""
        # Crop to question area
        cropped_image = self.image_processor.crop_image(image, CROPPED_IMAGE_BOX)
        cropped_bytes = self.image_processor.image_to_bytes(cropped_image)
        text = self.image_processor.extract_text_easyocr(cropped_bytes)

        # Try each question pattern
        for question_type, pattern in self.question_patterns.items():
            match = pattern.search(text)
            if match:
                answer = self._calculate_answer(question_type, match.groups())
                if answer is not None:
                    self._input_answer(str(answer))
                    return True

        return False

    def _calculate_answer(self, question_type: str, groups: tuple) -> Any:
        """Calculate answer based on question type."""
        try:
            if question_type == "addition":
                return int(groups[0]) + int(groups[1])
            elif question_type == "subtraction":
                return int(groups[0]) - int(groups[1])
            elif question_type == "multiplication":
                return int(groups[0]) * int(groups[1])
            elif question_type == "division":
                return int(groups[0]) // int(groups[1])  # Integer division
            elif question_type == "simple_equation":
                # For equations like x = 5, return the number
                return int(groups[1])
        except (ValueError, ZeroDivisionError) as e:
            self.logger.warning(f"Error calculating {question_type}: {e}")
            return None

        return None

    def _input_answer(self, answer: str) -> None:
        """Input the answer into the form."""
        try:
            # Try to find input field
            input_field = self.browser.driver.find_element(
                By.XPATH, "//input[@type='text' or @type='number']"
            )
            input_field.clear()
            input_field.send_keys(answer)

            # Submit the answer
            input_field.send_keys(Keys.RETURN)
            sleep(1)

        except Exception as e:
            # Fallback: send to body
            self.browser.driver.find_element(By.TAG_NAME, "body").send_keys(
                answer + Keys.RETURN
            )

    def _handle_unsolved_question(self) -> None:
        """Handle questions that couldn't be automatically solved."""
        # Try to find hint button
        try:
            hint_button = self.browser.driver.find_element(
                By.XPATH,
                "//button[contains(text(), 'Hint') or contains(text(), 'hint')]",
            )
            hint_button.click()
            sleep(2)
        except:
            # Try to skip
            try:
                skip_button = self.browser.driver.find_element(
                    By.XPATH,
                    "//button[contains(text(), 'Skip') or contains(text(), 'skip')]",
                )
                skip_button.click()
                sleep(2)
            except:
                # Random guess for multiple choice
                self._make_random_guess()

    def _make_random_guess(self) -> None:
        """Make a random guess for multiple choice questions."""
        try:
            choices = self.browser.driver.find_elements(
                By.XPATH,
                "//button[contains(@class, 'choice') or contains(@class, 'option')]",
            )
            if choices:
                import random

                random.choice(choices).click()
        except:
            pass

    def _check_completion(self, image: Image.Image) -> bool:
        """Check if all questions are completed."""
        text = self.image_processor.extract_text_pytesseract(image)
        completion_phrases = ["completed", "finished", "well done", "congratulations"]
        return any(phrase in text.lower() for phrase in completion_phrases)
