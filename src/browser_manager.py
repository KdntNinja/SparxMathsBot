"""Browser automation utilities for SparxMathsBot."""

import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BrowserManager:
    """Manages browser initialization and basic operations."""

    def __init__(self, headless: bool = True, timeout: int = 10):
        """Initialize browser with specified options."""
        self.timeout = timeout
        self.driver = self._initialize_browser(headless)
        self.wait = WebDriverWait(self.driver, timeout)

    def _initialize_browser(self, headless: bool) -> webdriver.Firefox:
        """Initialize Firefox browser with options."""
        options = Options()
        options.headless = headless

        firefox_bin = os.environ.get("FIREFOX_BINARY")
        if firefox_bin:
            options.binary_location = firefox_bin

        return webdriver.Firefox(options=options)

    def wait_for_element(
        self, by: By, value: str, clickable: bool = False
    ) -> Optional[webdriver.remote.webelement.WebElement]:
        """Wait for element to be present or clickable."""
        condition = (
            EC.element_to_be_clickable((by, value))
            if clickable
            else EC.presence_of_element_located((by, value))
        )
        return self.wait.until(condition)

    def get_screenshot_as_png(self) -> bytes:
        """Get screenshot as PNG bytes."""
        return self.driver.get_screenshot_as_png()

    def fullscreen(self) -> None:
        """Set browser to fullscreen."""
        self.driver.fullscreen_window()

    def quit(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
