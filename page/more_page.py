from appium.webdriver.common.appiumby import AppiumBy

from page.base_page import BasePage


class More(BasePage):
    def __init__(self, driver, platform=None):
        super().__init__(driver, platform)


    _more_tab = {
        "android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_More"]'),
        "ios": (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='More']"),
    }

    _more_title = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="My Stuff"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "My Stuff"),
    }

    _sign_out = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Sign Out"]'),
        "ios": (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Sign Out"]'),
    }

    _sign_out_yes = {
        "android": (AppiumBy.XPATH, "//android.widget.TextView[@text='Do you want to logout']/following::android.widget.Button[1]"),
        "ios": (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Yes"]'),
    }

    _sign_out_no = {
        "android": (AppiumBy.XPATH, "//android.widget.TextView[@text='Do you want to logout']/following::android.widget.Button[2]"),
        "ios": (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="No"]'),
    }

    _version = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text, "Version:")]'),
        "ios": (AppiumBy.XPATH, '//XCUIElementTypeStaticText[starts-with(@name, "App version :")]'),
    }

    def click_more_tab(self):
        self.click(self._more_tab)

    def is_more_screen_title_displayed(self):
        return self.is_displayed(self._more_title)

    def click_sign_out(self):
        if BasePage.is_displayed(self, self._sign_out,2):
            BasePage.tap(self, self._sign_out)
        else:
            self.scroll_to_bottom()
            self.click(self._sign_out)

    def confirm_sign_out(self):
        self.tap(self._sign_out_yes)

    def cancel_sign_out(self):
        self.tap(self._sign_out_no)

    def get_app_version(self):
        return self.get_text(self._version)

    def is_app_version_displayed(self):
        return self.is_displayed(self._version)



