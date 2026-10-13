import time

from appium.webdriver.common.appiumby import AppiumBy
from page.base_page import BasePage


class Home(BasePage):
    def __init__(self, driver, platform=None):
        super().__init__(driver, platform)


    _sign_create_account = {
        "android": (AppiumBy.XPATH,"//android.view.View[@resource-id='auto_sign_in_button']",),
        "ios": (AppiumBy.XPATH, "//XCUIElementTypeButton[@name='auto_sign_in_card']"),
    }
    _manage_account = {
        "android": (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='auto_greeting_manage_account']"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "auto_greeting_manage_account"),
    }

    _guest_search = {
        "android": (AppiumBy.XPATH, '//*[@content-desc="Images/Home/search" or @resource-id="Images/Home/search"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Images/Home/search"),
    }
    _guest_welcome = {
        "android": (AppiumBy.XPATH, '//*[@content-desc="WELCOME" or @text="WELCOME"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "WELCOME"),
    }



    def click_sign_in_create_account(self):
        time.sleep(5)
        if self.is_displayed(self._sign_create_account, timeout=5):
            self.fluent_click(self._sign_create_account)

    def is_sign_in_button_displayed(self):
        return self.is_displayed(self._sign_create_account, timeout=5)

    def get_manage_account_text(self):
        return self.get_text(self._manage_account)

    def verify_home_screen_loaded(self):
        return self.is_displayed(self._manage_account)

    def verify_guest_home(self):
        return self.is_displayed(self._guest_search) and self.is_displayed(self._guest_welcome)

    def is_manage_account_displayed(self):
        time.sleep(5)
        return self.is_displayed(self._manage_account)
