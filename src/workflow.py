import io
import re
import os
from random import uniform
from time import sleep
from typing import Callable, List

import easyocr  # type: ignore
import pyautogui
import pytesseract  # type: ignore
import resend
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from .config import *
from .decorators import log_function_call
from .logger_setup import setup_logger

logger = setup_logger()


class SparxTTWorkflow:
    def __init__(self) -> None:
        logger.debug("Initializing SparxTTWorkflow...")
        self.driver: webdriver.Firefox = webdriver.Firefox()
        self.wait: WebDriverWait[webdriver.Firefox] = WebDriverWait(self.driver, 10)
        logger.debug("Web driver initialized and WebDriverWait set.")
        logger.debug("Workflow attributes set.")

    @log_function_call
    def run_workflow(self) -> None:
        logger.info("Running workflow...")
        self.driver.fullscreen_window()
        try:
            self.select_school()
            self.login()
            self.get_to_tt()
            self.click_start_quiz()
            self.solve_quiz()
            sleep(3)
        except Exception as e:
            logger.error(f"An error occurred during the workflow: {e}", exc_info=True)
        finally:
            self.cleanup()
            logger.info("Workflow run completed, cleanup executed.")

    @log_function_call
    def execute_step(self, step_func: Callable[[], None]) -> None:
        try:
            step_func()
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Error in {step_func.__name__}: {e}", exc_info=True)

    @log_function_call
    def select_school(self) -> None:
        logger.debug(f"Opening school URL: {SCHOOL_URL}")
        self.driver.get(SCHOOL_URL)
        input_element = self.wait_for_element(By.CLASS_NAME, SCHOOL_INPUT_CLASS_NAME)
        input_element.send_keys(SCHOOL_TEXT + Keys.RETURN)
        continue_button = self.wait_for_element(
            By.XPATH, "//button[text()='Continue']", clickable=True
        )
        continue_button.click()
        logger.info("School selection complete.")

    @log_function_call
    def login(self) -> None:
        self.wait_for_element(By.ID, USERNAME_ID).send_keys(USERNAME)
        self.wait_for_element(By.ID, PASSWORD_ID).send_keys(PASSWORD + Keys.RETURN)
        logger.debug("Login attempted.")

    @log_function_call
    def get_to_tt(self) -> None:
        self.wait_for_element(
            By.CLASS_NAME, HOMEWORK_TEXT_CLASS_NAME, clickable=True
        ).click()
        self.wait_for_element(By.XPATH, TIMES_TABLES_TEXT_XPATH, clickable=True).click()
        self.wait_for_element(By.XPATH, CLUB_CHECK_TEXT_XPATH, clickable=True).click()
        sleep(10)
        logger.info("Successfully navigated to Times Tables.")

    @log_function_call
    def click_start_quiz(self) -> None:
        text_to_find: str = "Start quiz"
        logger.debug("Entering loop to find and click start quiz button.")
        while True:
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            extracted_text = pytesseract.image_to_string(image)
            if text_to_find in extracted_text:
                logger.debug("Start quiz button found. Proceeding to click it.")
                pyautogui.click(*START_BUTTON_LOCATION)
                break
        logger.info("Successfully clicked start quiz button.")

    @log_function_call
    def solve_quiz(self) -> None:
        pattern = re.compile(r"(\d+)\s*\*\s*(\d+)\s*=\s*\?")
        reader = easyocr.Reader(["en"], gpu=True)
        successful_attempts = 0

        while successful_attempts < 60:
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            cropped_image = image.crop(CROPPED_IMAGE_BOX)

            cropped_image_bytes = io.BytesIO()
            cropped_image.save(cropped_image_bytes, format="PNG")
            cropped_image_bytes.seek(0)

            # EasyOCR with detail=0 and paragraph=True returns List[str]
            extracted_text_result: List[str] = reader.readtext(
                cropped_image_bytes.getvalue(), detail=0, paragraph=True
            )

            # Convert all text results to strings and join them
            extracted_text: List[str] = [str(item) for item in extracted_text_result]

            match = pattern.search(" ".join(extracted_text))

            if successful_attempts % 10 == 0:
                pyautogui.click(*START_BUTTON_LOCATION)

            if match:
                num1, num2 = map(int, match.groups())
                result = num1 * num2

                sleep(uniform(2, 3.5))

                self.driver.find_element(By.TAG_NAME, "body").send_keys(
                    str(result) + Keys.RETURN
                )
                successful_attempts += 1

                if successful_attempts == 25 or successful_attempts == 50:
                    self.wait_for_element(
                        By.XPATH, TIMES_TABLES_EXIT_XPATH, clickable=True
                    ).click()
                    self.wait_for_element(
                        By.XPATH, CLUB_CHECK_TEXT_XPATH, clickable=True
                    ).click()
                    self.click_start_quiz()

    @log_function_call
    def wait_for_element(
        self, by: By, value: str, clickable: bool = False
    ) -> WebElement:
        condition = (
            EC.element_to_be_clickable((by, value))
            if clickable
            else EC.presence_of_element_located((by, value))
        )
        return self.wait.until(condition)

    @log_function_call
    def cleanup(self) -> None:
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Web driver closed.")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}", exc_info=True)
            finally:
                resend.api_key = RESEND_API_KEY
                log_file_path = os.path.join("build", "workflow_log.txt")
                resend.Emails.send(
                    {
                        "from": "SparxTT-Solver@resend.dev",
                        "to": RESEND_TO,
                        "subject": "SparxTT-Solver Finished",
                        "html": "<p>SparxTT-Solver Run <strong>Finished</strong>!</p><pre>"
                        + "".join(reversed(open(log_file_path, "r").readlines()))
                        + "</pre>",
                    }
                )
                logger.info("Email sent.")
