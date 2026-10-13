from appium.webdriver.common.appiumby import AppiumBy

from page.base_page import BasePage


class Login(BasePage):
    def __init__(self, driver, platform=None):
        super().__init__(driver, platform)

    # --- USER INTERACTIONS & VERIFICATIONS ---
    def verify_email_screen_ui(self):
        return self.is_displayed(self._email_title) and self.is_displayed(self._email_subtitle)

    def enter_email(self, email):
        self.send_keys_to_element(self._email_textbox, email)

    def click_email_submit(self):
        self.click(self._email_submit)

    def click_continue_as_guest(self):
        self.click(self._email_guest_button)

    def get_email_error_msg(self):
        return self.get_text(self._email_error_msg)

    def is_email_error_displayed(self):
        return self.is_displayed(self._email_error_msg, timeout=5)

    def verify_password_screen_loaded(self):
        return self.is_displayed(self._password_title)

    def get_displayed_email_text(self):
        return self.get_text(self._password_displayed_email)

    def enter_password(self, password):
        self.send_keys_to_element(self._password_textbox, password)

    def click_password_submit(self):
        self.hide_keyboard()
        self.click(self._password_submit)

    def is_forgot_password_displayed(self):
        return self.is_displayed(self._forgot_password_button)

    def get_password_error_msg(self):
        return self.get_text(self._password_error_msg)

    def is_password_error_displayed(self):
        return self.is_displayed(self._password_error_msg, timeout=5)

    def get_email_title_text(self):
        self.wait_for_visible_element(self._email_title,10)
        return self.get_text(self._email_title)

    def get_email_subtitle_text(self):
        return self.get_text(self._email_subtitle)

    def get_password_title_text(self):
        return self.get_text(self._password_title)
    def get_password_subtitle_text(self):
        return self.get_text(self._password_subtitle)

    def is_email_textbox_displayed(self):
        return self.is_displayed(self._email_textbox)

    def is_guest_button_displayed(self):
        return self.is_displayed(self._email_guest_button)

    def is_password_textbox_displayed(self):
        return self.is_displayed(self._password_textbox)


    # --- ENTER EMAIL SCREEN LOCATORS ---
    _email_title = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_LoginTitle"]'),
        "ios": (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='auto_LoginTitle']"),
    }
    _email_subtitle = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_LoginDescription"]'),
        "ios": (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='auto_LoginDescription']"),
    }
    _email_textbox = {
        "android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_EmailInputField"]'),
        "ios": (AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"),
    }
    _email_submit = {
        "android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_ContinueButton"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "auto_ContinueButton"),
    }
    _email_guest_button = {
        "android": (AppiumBy.XPATH, '//*[@resource-id="auto_ContinueAsGuestButton"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "auto_ContinueAsGuestButton"),
    }
    _email_error_msg = {
        "android": (AppiumBy.XPATH,'//*[@resource-id="auto_EmailInputFieldError" or @text="Invalid email address."]'),
        "ios": (AppiumBy.XPATH, "auto_EmailInputFieldError"),
    }

    # --- ENTER PASSWORD SCREEN LOCATORS ---
    _password_title = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_PasswordTitle"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "auto_PasswordTitle"),
    }
    _password_subtitle = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Enter Your Password to Continue."]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Enter Your Password to Continue."),
    }
    _password_displayed_email = {
        "android": (AppiumBy.XPATH, "(//android.widget.TextView[@text='Enter Your Password to Continue.']/following::android.widget.TextView)[1]"),
        "ios": (AppiumBy.XPATH, "(//XCUIElementTypeStaticText)[3]"),
    }
    _password_textbox = {
        "android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_PasswordInputField"]'),
        "ios": (AppiumBy.CLASS_NAME, 'XCUIElementTypeSecureTextField'),
    }
    _forgot_password_button = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_ForgotPasswordText"]'),
        "ios": (AppiumBy.XPATH, "//XCUIElementTypeButton[@name='auto_ForgotPasswordText']"),
    }
    _password_submit = {
        "android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_LoginButton"]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "auto_LoginButton"),
    }
    _password_error_msg = {
        "android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Incorrect username or password."]'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Incorrect username or password."),
    }



