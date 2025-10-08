import io
import logging
import os
import re
from functools import wraps
from random import uniform
from time import sleep
from typing import Callable, Any

import easyocr  # type: ignore
import pyautogui
import pytesseract  # type: ignore
import resend
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

# Load environment variables
load_dotenv()

# --- Logging Setup ---
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("workflow_log.txt", mode="w")

console_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger("SparxTTWorkflow")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# --- Constants ---
START_BUTTON_LOCATION = (958, 914)
CROPPED_IMAGE_BOX = (724, 139, 1205, 215)  # (left, upper, right, lower)


# --- Decorators ---
def log_function_call(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Entering function: {func.__name__}")
        try:
            result = func(self, *args, **kwargs)
            logger.debug(f"Exiting function: {func.__name__}")
            return result
        except Exception as e:
            logger.exception(f"Error in function '{func.__name__}': {e}")
            raise

    return wrapper


# --- Main Workflow Class ---
class SparxTTWorkflow:
    def __init__(self) -> None:
        logger.debug("Initializing SparxTTWorkflow...")
        self.driver: webdriver.Firefox = webdriver.Firefox()
        self.wait: WebDriverWait[webdriver.Firefox] = WebDriverWait(self.driver, 10)
        logger.debug("Web driver initialized and WebDriverWait set.")

        # School Selection
        self.school_url: str = "https://selectschool.sparxmaths.uk/?forget=1"
        self.school_text: str = os.getenv("SCHOOL_TEXT", "")
        self.school_input_class_name: str = "_Input_14i1t_4"

        # Login
        self.username_text: str = os.getenv("USERNAME", "")
        self.password_text: str = os.getenv("PASSWORD", "")
        self.username_id: str = "username"
        self.password_id: str = "password"
        self.login_button_class_name: str = "sm-button login-button"

        # Navigation
        self.homework_text_class_name: str = "_PackageLeft_s1pvn_28"
        self.start_button_xpath: str = (
            "//a[contains(@class, '_Task_1p2y5_1')]//div[contains(@class, '_TaskChip_1p2y5_79') and text()='Start']"
        )
        self.times_tables_text_xpath: str = "//span[contains(text(), 'Times Tables')]"
        self.club_check_text_xpath: str = (
            "//div[contains(@class, '_Content_nt2r3_194') and text()='100 Club Check']"
        )
        self.times_tables_exit_xpath: str = (
            "//a[contains(@class, '_BackButton_1iso5_1')]"
        )
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
        logger.debug(f"Opening school URL: {self.school_url}")
        self.driver.get(self.school_url)
        input_element = self.wait_for_element(
            By.CLASS_NAME, self.school_input_class_name
        )
        input_element.send_keys(self.school_text + Keys.RETURN)
        continue_button = self.wait_for_element(
            By.XPATH, "//button[text()='Continue']", clickable=True
        )
        continue_button.click()
        logger.info("School selection complete.")

    @log_function_call
    def login(self) -> None:
        self.wait_for_element(By.ID, self.username_id).send_keys(self.username_text)
        self.wait_for_element(By.ID, self.password_id).send_keys(
            self.password_text + Keys.RETURN
        )
        logger.debug("Login attempted.")

    @log_function_call
    def get_to_tt(self) -> None:
        self.wait_for_element(
            By.CLASS_NAME, self.homework_text_class_name, clickable=True
        ).click()
        self.wait_for_element(
            By.XPATH, self.times_tables_text_xpath, clickable=True
        ).click()
        self.wait_for_element(
            By.XPATH, self.club_check_text_xpath, clickable=True
        ).click()
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

            extracted_text_result = reader.readtext(
                cropped_image_bytes.getvalue(), detail=0, paragraph=True
            )
            
            # Handle the different possible return types from EasyOCR
            if isinstance(extracted_text_result, list):
                # Convert all elements to strings to ensure compatibility with join
                extracted_text = [str(item) for item in extracted_text_result]
            else:
                extracted_text = [str(extracted_text_result)]
            
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
                        By.XPATH, self.times_tables_exit_xpath, clickable=True
                    ).click()
                    self.wait_for_element(
                        By.XPATH, self.club_check_text_xpath, clickable=True
                    ).click()
                    self.click_start_quiz()

    @log_function_call
    def wait_for_element(
        self, by: By, value: str, clickable: bool = False
    ) -> WebElement:
        condition = (
            EC.element_to_be_clickable((by.value, value))
            if clickable
            else EC.presence_of_element_located((by.value, value))
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
                resend.api_key = os.getenv("RESEND_API_KEY", "")
                resend_to = os.getenv("RESEND_TO", "")
                resend.Emails.send(
                    {
                        "from": "SparxTT-Solver@resend.dev",
                        "to": resend_to,
                        "subject": "SparxTT-Solver Finished",
                        "html": "<p>SparxTT-Solver Run <strong>Finished</strong>!</p><pre>"
                        + "".join(reversed(open("workflow_log.txt", "r").readlines()))
                        + "</pre>",
                    }
                )
                logger.info("Email sent.")


if __name__ == "__main__":
    sparx = SparxTTWorkflow()
    sparx.run_workflow()
    logger.info("Workflow run completed.")