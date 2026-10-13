import time

from appium.webdriver.common.appiumby import AppiumBy

from fixtures.driver import driver
from page import base_page
from page.base_page import BasePage


class Signup(BasePage):
    def __init__(self, driver, platform=None):
        super().__init__(driver, platform)

# get text
    def signup_botton_sheet_title(self):
    #Email Not Found
        return self.get_text(self._signup_botton_sheet_title)

    def get_signup_botton_sheet_description(self):
    #If you had a Six Flags MyPass account, you’ll need to create a new account. Don’t worry, any tickets stored in your app will reappear once your account is set up!
        return self.get_text(self._signup_botton_sheet_description)

    def get_signup_form_title(self):
    #Create An Account
        return self.get_text(self._signup_form_title)

    def get_signup_description(self):
    #To get started, enter the information\nbelow.
        return self.get_text(self._signup_description)

    def get__invalid_phone_number_error(self):
        return self.get_text(self._invalid_phone_number_error)

    def get_email_id(self):
        self.hide_keyboard()
        return self.get_text(self._entered_email)



#is Displayed methods
    def is_signup_bottom_sheet_ui_elements_displayed(self):
        return (self.is_displayed(self._signup_botton_sheet_title) and
        self.is_displayed(self._signup_botton_sheet_description) and
        self.is_displayed(self._signup_button) and
        self.is_displayed(self._continue_as_guest))

    def is_signup_form1_ui_elements_displayed(self):
        return (self.is_displayed(self._signup_screen_title) and
        self.is_displayed(self._signup_form_title) and
        self.is_displayed(self._signup_description) and
        self.is_displayed(self._first_name_placeholder) and
        self.is_displayed(self._last_name_placeholder) and
        self.is_displayed(self._date_of_birth_placeholder) and
        self.is_displayed(self._email_placeholder) and
        self.is_displayed(self._home_park_placeholder))


    def is_name_warning_displayed(self):
        return self.is_displayed(self._signup_form_title)

#sent keys
    def enter_first_name(self, first_name):
        self.send_keys_to_element(self._first_name_textbox,first_name)

    def enter_last_name(self, last_name):
        self.send_keys_to_element(self._last_name_textbox,last_name)


# Functions
    def click_signup_bottom_sheet_submit(self):
        self.tap(self._signup_button)

    def enter_dob(self):
        if self.platform == "android":
            self.click(self._calender)
            self.click(self._pick_date_android)
            self.click(self._select_date_android)
        elif self.platform == "ios":
            print("coming soon")

        time.sleep(2)
        self.hide_keyboard()


    def select_home_park(self,park_name):
        self.tap(self._home_park_list,5)
        locator = self.format_locator(self._select_home_park, park_name)
        self.click(locator)
        self.hide_keyboard()

    _parks_with_phone_number = {
        "Carowinds",
        "Cedar Point",
        "Kings Dominion",
        "Kings Island",
        "Knott's Berry Farm",
        "Six Flags Discovery Kingdom",
        "Six Flags Fiesta Texas",
        "Six Flags Great America",
        "Six Flags Magic Mountain",
        "Six Flags Over Texas",
    }

    def verify_phone_field_visibility(self, park_name, phone_number=None):
        phone_should_be_visible = park_name in self._parks_with_phone_number
        is_visible = self.is_element_present(self._phone_number_textbox)

        if phone_should_be_visible:
            assert is_visible, f"Expected phone field to be DISPLAYED for '{park_name}', but it was HIDDEN."
            if phone_number:
                self.send_keys_to_element(self._phone_number_textbox, phone_number)
        else:
            assert not is_visible, f"Expected phone field to be HIDDEN for '{park_name}', but it was DISPLAYED."
        return True

    def select_park_and_verify_phone(self, park_name, phone_number=None):
        # 1. Select the park
        self.select_home_park(park_name)
        return self.verify_phone_field_visibility(park_name, phone_number)

    def enter_password(self, password):
        self.scroll_to_bottom()
        self.send_keys_to_element(self._password_textbox, password)
        self.tap(self._show_password)

    def confirm_password(self, password):
        self.send_keys_to_element(self._confirm_password_textbox, password)
        self.tap(self._show_password)


    def password_missmatch_error_displayed(self):
        return self.is_displayed(self._password_missmatch_error)

    def check_sms_option(self ):
        self.tap(self._sms_option_checkbox)

    def check_email_option(self):
        self.tap(self._email_option_checkbox)

    def uncheck_sms_option(self):
        self.tap(self._sms_option_checkbox)

    def uncheck_email_option(self):
        self.tap(self._email_option_checkbox)

    def click_create_account_button(self):
        self.tap(self._create_account_button)


    # --- Signup Bottom sheet ---

    _signup_botton_sheet_title = {"android": (AppiumBy.XPATH, '(//android.widget.TextView[1])[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _signup_botton_sheet_description = {"android": (AppiumBy.XPATH, '//android.widget.TextView[2]'),
        "ios": (AppiumBy.XPATH, ""),}

    _signup_button = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Sign Up"]/following::android.widget.Button[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _continue_as_guest = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Sign Up"]/following::android.widget.Button[2]'),
        "ios": (AppiumBy.XPATH, ""),}

    # --- Signup form  ---

    _signup_screen_title = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_SignUpTitle"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _signup_form_title = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_SignUpTitle"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _signup_description = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="auto_SignUpDescription"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _first_name_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="First Name*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _first_name_textbox = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_FirstNameInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _name_error = {"android": (AppiumBy.XPATH, "//android.widget.TextView[@text='Please fill in this field.']"),
        "ios": (AppiumBy.XPATH, "")}

    _last_name_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Last Name*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _last_name_textbox = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_LastNameInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _date_of_birth_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Date of Birth*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _calender = {"android": (AppiumBy.XPATH, '//android.view.View[@content-desc="Calender"]'),
        "ios": (AppiumBy.XPATH, ""),}

    # By default, 2nd of every month

    _pick_date_android = {"android": (AppiumBy.XPATH, '(//android.widget.Button)[5]'),
        "ios": (AppiumBy.XPATH, ""),}

    _select_date_android = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Select"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _email_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Email*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _entered_email = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_EmailInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _home_park_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Home Park*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _home_park_list = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_HomeParkInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _select_home_park = {"android": (AppiumBy.XPATH,'//android.widget.TextView[@text="{}"]'),
        "ios": (AppiumBy.XPATH,'//XCUIElementTypeStaticText[@name="{}"]')}

    _phone_number_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Phone Number"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _phone_number_textbox = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_PhoneNumberInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _invalid_phone_number_error = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Please enter valid phone number."]'),
        "ios": (AppiumBy.XPATH, ""),}

    #scroll to bottom to view these elements

    _password_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Password*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _password_textbox = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_PasswordInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _confirm_password_placeholder = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Confirm Password*"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _confirm_password_textbox = {"android": (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="auto_SignUp_ConfirmPasswordInputField"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _password_missmatch_error = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Please enter valid phone number."]'),
        "ios": (AppiumBy.XPATH, ""),}

    _show_password = {"android": (AppiumBy.XPATH, '(//android.view.View[@content-desc="Show password"])[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _hide_password = {"android": (AppiumBy.XPATH, '(//android.view.View[@content-desc="Hide password"])[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _email_option_checkbox = {"android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_SignUp_EmailOptInCheckbox"]/android.widget.CheckBox'),
        "ios": (AppiumBy.XPATH, ""),}

    _sms_option_checkbox = {"android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_SignUp_SMSOptInCheckbox"]/android.widget.CheckBox'),
        "ios": (AppiumBy.XPATH, ""),}

    _email_option_text = {"android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_SignUp_EmailOptInCheckbox"]/android.widget.TextView'),
        "ios": (AppiumBy.XPATH, ""),}

    _sms_option_text = {"android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_SignUp_SMSOptInCheckbox"]/android.widget.TextView'),
        "ios": (AppiumBy.XPATH, ""),}

    _create_account_button = {"android": (AppiumBy.XPATH, '//android.view.View[@resource-id="auto_SignUp_CreateAccountButton"]/android.view.View/android.widget.Button'),
        "ios": (AppiumBy.XPATH, ""),}

    #signup OTP

    _otp_sheet_title = {"android": (AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.TextView[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _opt_sheet_description = {"android": (AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.TextView[2]'),
        "ios": (AppiumBy.XPATH, ""), }

    _enter_otp = {"android": (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.View/android.widget.EditText[1]'),
        "ios": (AppiumBy.XPATH, ""),}

    _clear_otp = {"android": (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.View/android.widget.EditText[6]'),
        "ios": (AppiumBy.XPATH, ""),}

    _submit_button = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Submit"]/following::android.widget.Button'),
        "ios": (AppiumBy.XPATH, ""),}

    _otp_error = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Invalid verification code provided, please try again."]'),
        "ios": (AppiumBy.XPATH, ""),}

    _resent_code = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Resend Code"]'),
        "ios": (AppiumBy.XPATH, ""),}

    #success screen

    _success_title = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="Account created"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _success_description = {"android": (AppiumBy.XPATH, '//android.widget.TextView[@text="You have successfully created an account"]'),
        "ios": (AppiumBy.XPATH, ""),}

    _login_button = {"android": (AppiumBy.XPATH, '//android.widget.Button'),
        "ios": (AppiumBy.XPATH, ""),}


""""carowinds , Cedar Point , Kings Dominion , Kings Island ,Knott's Berry Farm , Six Flags Discovery Kingdom , Six Flags Fiesta Texas , Six Flags Grate America ,  Six Flags Magic Mountain , Six Flags Texas these parks have phone number field """