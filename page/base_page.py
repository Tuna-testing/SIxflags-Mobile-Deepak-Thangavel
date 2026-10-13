from datetime import datetime

from selenium.common import NoSuchElementException, TimeoutException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.gesture import Gesture


class BasePage:
    def __init__(self, driver, platform=None):
        self.driver = driver
        self.gesture = Gesture(self.driver)
        # Dynamically resolve platform if not explicitly passed
        self.platform = (platform or driver.capabilities.get("platformName", "")).lower()

        # Read default timeout or fallback to 30s
        config_timeout = "60"
        self.default_timeout: int = int(config_timeout) if config_timeout else 30
        self.wait = WebDriverWait(self.driver, self.default_timeout)

    @staticmethod
    def get_formatted_time() -> str:
        return datetime.now().strftime("%Y%m%d%H%M")

    @classmethod
    def get_email_id(cls) -> str:
        return f"olivefrancine+uat{cls.get_formatted_time()}@chefalicious.com"

    def _get_locator(self, locator_map):
        """Resolves locator tuple based on current platform."""
        if isinstance(locator_map, dict):
            return locator_map[self.platform]
        return locator_map

    # ==========================================
    # 🔍 EXPLICIT WAITS & ELEMENT FINDING
    # ==========================================
    def wait_for_element(self, locator_map, timeout=None):
        """Wait for element presence in the DOM."""
        by, value = self._get_locator(locator_map)
        t = timeout or self.default_timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_visible_element(self, locator_map, timeout=None):
        """Wait for element to be visible on screen."""
        by, value = self._get_locator(locator_map)
        t = timeout or self.default_timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located((by, value))
        )

    def fluent_click(self, locator_map, timeout=10, poll_frequency=0.5):
        """Reusable fluent wait click that automatically ignores stale element errors during DOM refreshes."""
        by, value = self._get_locator(locator_map)

        wait = WebDriverWait(
            self.driver,
            timeout=timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=(
                StaleElementReferenceException,
                ElementClickInterceptedException,
            ),
        )

        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def _find_element(self, locator_dict, timeout=None):
        return self.wait_for_element(locator_dict, timeout)

    def is_element_present(self, locator_map):
        try:
            by, value = self._get_locator(locator_map)
            return bool(
                WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located((by, value))
                )
            )
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return False

    # ==========================================
    # ⚡ CORE ELEMENT ACTIONS
    # ==========================================
    def click(self, locator_map, timeout=None):
        element = self.wait_for_visible_element(locator_map, timeout)
        element.click()

    def send_keys_to_element(self, locator_map, text, timeout=None):
        element = self.wait_for_visible_element(locator_map, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator_map, timeout=None):
        return self.wait_for_visible_element(locator_map, timeout).text

    def is_displayed(self, locator_map, timeout=None):
        try:
            element = self.wait_for_visible_element(locator_map, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    @staticmethod
    def format_locator(locator_map: dict, *args) -> dict:
        """Injects dynamic values (*args) into string placeholders inside a locator map."""
        return {
            platform: (by, locator_str.format(*args))
            for platform, (by, locator_str) in locator_map.items()
        }
    # ==========================================
    # 📱 WRAPPED MOBILE GESTURES
    # ==========================================
    def tap(self, locator_map, timeout=None):
        element = self.wait_for_visible_element(locator_map, timeout)
        self.gesture.tap( element)

    def scroll_up(self):
        self.gesture.scroll_up()

    def scroll_down(self):
        self.gesture.scroll_down()

    def swipe_left(self):
        self.gesture.swipe_left()

    def swipe_right(self):
        self.gesture.swipe_right()

    def scroll_to_element(self, locator_map, max_scrolls=20):
        locator = self._get_locator(locator_map)
        self.gesture.scroll_to_element(locator, max_scrolls=max_scrolls)

    def scroll_to_top(self):
        self.gesture.scroll_to_top()

    def scroll_to_bottom(self):
        self.gesture.scroll_to_bottom()

    def drag_and_drop(self, source_locator_map, target_locator_map, timeout=None):
        source_element = self.wait_for_visible_element(source_locator_map, timeout)
        target_element = self.wait_for_visible_element(target_locator_map, timeout)
        self.gesture.drag_and_drop(source_element, target_element)

    def hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
            if self.platform == "android":
             self.driver.execute_script("mobile: hideKeyboard")
            elif self.platform == "ios":
              self.driver.hide_keyboard()
        except (TimeoutException, NoSuchElementException):
            return False


