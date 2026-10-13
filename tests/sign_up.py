import time

from pytest_bdd import step

from page.base_page import BasePage
from page.home import Home
from page.login_page import Login
from page.sign_up import Signup


# scenarios('../features/signup.feature')
import logging
logger = logging.getLogger(__name__)
@step("User enters an unregistered email and submits")
def enter_unregistered_email(home_page: Home, login_page: Login):
    logger.info("\n[STEP START] User enters an unregistered email and submits", flush=True)

    logger.info("[ACTION] Generating random email via BasePage...", flush=True)
    email = BasePage.get_email_id()
    logger.info(f"[DATA] Generated email: {email}", flush=True)

    logger.info("[ACTION] Checking if Sign-In button is displayed on Home page...", flush=True)
    if home_page.is_sign_in_button_displayed():
        logger.info("[INFO] Home screen loaded. Clicking Sign In / Create Account...", flush=True)
        home_page.click_sign_in_create_account()
        time.sleep(3)
    else:
        logger.info("[INFO] Already on email screen or Sign-In button not present.", flush=True)

    logger.info(f"[ACTION] Entering email '{email}' into login page...", flush=True)
    login_page.enter_email(email)

    logger.info("[ACTION] Clicking submit on email screen...", flush=True)
    login_page.click_email_submit()
    time.sleep(2)
    logger.info("[STEP END] Finished entering unregistered email and submitting", flush=True)


@step("User verifies the UI elements for the signup bottom sheet")
def verify_bottom_sheet_ui(signup_page: Signup):
    logger.info("\n[STEP START] User verifies the UI elements for the signup bottom sheet", flush=True)

    logger.info("[ACTION] Verifying UI elements presence on bottom sheet...", flush=True)
    signup_page.is_signup_bottom_sheet_ui_elements_displayed()

    logger.info("[FETCH] Reading actual title from bottom sheet...", flush=True)
    actual_title = signup_page.signup_botton_sheet_title()
    logger.info(f"[DATA] Actual title fetched: '{actual_title}'", flush=True)

    logger.info("[FETCH] Reading actual subtitle from bottom sheet...", flush=True)
    actual_subtitle = signup_page.get_signup_botton_sheet_description()
    logger.info(f"[DATA] Actual subtitle fetched: '{actual_subtitle}'", flush=True)

    expected_title = "Email Not Found"
    expected_subtitle = "If you had a Six Flags MyPass account, you’ll need to create a new account. Don’t worry, any tickets stored in your app will reappear once your account is set up!"

    logger.info(f"[ASSERT] Validating '{expected_title}' in actual title...", flush=True)
    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in '{actual_title}'"

    logger.info(f"[ASSERT] Validating expected subtitle presence...", flush=True)
    assert expected_subtitle in actual_subtitle, f"Expected subtitle '{expected_subtitle}' not found in '{actual_subtitle}'"

    logger.info("[STEP END] User verified the UI elements for the signup bottom sheet successfully", flush=True)


@step("User clicks submit on the signup bottom sheet")
def submit_bottom_sheet(signup_page: Signup):
    logger.info("\n[STEP START] User clicks submit on the signup bottom sheet", flush=True)
    logger.info("[ACTION] Clicking bottom sheet submit button...", flush=True)
    signup_page.click_signup_bottom_sheet_submit()
    logger.info("[STEP END] User clicked submit on the signup bottom sheet", flush=True)


@step("User verifies the UI elements for the signup form")
def verify_signup_form_ui(signup_page: Signup):
    logger.info("\n[STEP START] User verifies the UI elements for the signup form", flush=True)

    logger.info("[ACTION] Verifying Form 1 UI elements...", flush=True)
    signup_page.is_signup_form1_ui_elements_displayed()

    logger.info("[FETCH] Reading actual title from signup form...", flush=True)
    actual_title = signup_page.get_signup_form_title()
    logger.info(f"[DATA] Actual form title: '{actual_title}'", flush=True)

    expected_title = "Welcome To Six Flags!"
    logger.info(f"[ASSERT] Validating '{expected_title}' in actual title...", flush=True)
    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in '{actual_title}'"

    logger.info("[STEP END] User verified the UI elements for the signup form successfully", flush=True)


@step("User enters an invalid first name and verifies the error message")
def enter_invalid_first_name(signup_page: Signup):
    logger.info("\n[STEP START] User enters an invalid first name and verifies the error message", flush=True)

    logger.info("[ACTION] Entering space character as invalid first name...", flush=True)
    signup_page.enter_first_name(" ")

    logger.info("[ACTION/ASSERT] Verifying name warning display...", flush=True)
    signup_page.is_name_warning_displayed()

    logger.info("[ACTION] Clearing field by entering 'Test'...", flush=True)
    signup_page.enter_first_name("Test")

    logger.info("[STEP END] Finished invalid first name verification", flush=True)


@step("User enters a valid first name")
def enter_valid_first_name(signup_page: Signup):
    logger.info("\n[STEP START] User enters a valid first name", flush=True)
    logger.info("[ACTION] Entering 'Test' into First Name field...", flush=True)
    signup_page.enter_first_name("Test")
    logger.info("[STEP END] User entered a valid first name", flush=True)


@step("User enters an invalid last name and verifies the error message")
def enter_invalid_last_name(signup_page: Signup):
    logger.info("\n[STEP START] User enters an invalid last name and verifies the error message", flush=True)

    logger.info("[ACTION] Entering space character as invalid last name...", flush=True)
    signup_page.enter_last_name(" ")

    logger.info("[ACTION/ASSERT] Verifying name warning display...", flush=True)
    signup_page.is_name_warning_displayed()

    logger.info("[STEP END] Finished invalid last name verification", flush=True)


@step("User enters a valid last name")
def enter_valid_last_name(signup_page: Signup):
    logger.info("\n[STEP START] User enters a valid last name", flush=True)
    logger.info("[ACTION] Entering 'Test' into Last Name field...", flush=True)
    signup_page.enter_last_name("Test")
    logger.info("[STEP END] User entered a valid last name", flush=True)


@step("User selects date of birth")
def select_dob(signup_page: Signup):
    logger.info("\n[STEP START] User selects date of birth", flush=True)
    logger.info("[ACTION] Executing enter_dob()...", flush=True)
    signup_page.enter_dob()
    logger.info("[STEP END] User selected date of birth", flush=True)


@step("User selects a park with phone number and enters the phone number")
def select_park_with_phone(signup_page: Signup):
    logger.info("\n[STEP START] Selecting park with phone number...", flush=True)
    logger.info("[ACTION] Selecting 'Carowinds' and verifying phone '8870344201'...", flush=True)
    signup_page.select_park_and_verify_phone("Carowinds", "8870344201")
    logger.info("[STEP END] Finished selecting Carowinds", flush=True)


@step("User selects a park without phone number")
def select_park_without_phone(signup_page: Signup):
    logger.info("\n[STEP START] Selecting a park without phone number...", flush=True)

    logger.info("[ACTION] Selecting 'Dorney Park'...", flush=True)
    signup_page.select_park_and_verify_phone("Dorney Park")
    time.sleep(1)

    logger.info("[ACTION] Switching selection to 'Cedar Point' with phone '8870344201'...", flush=True)
    signup_page.select_park_and_verify_phone("Cedar Point", "8870344201")
    time.sleep(1)

    logger.info("[STEP END] Finished selecting park without phone number sequence", flush=True)


@step("User enters a valid password and shows the password")
def enter_password_and_show(signup_page: Signup):
    logger.info("\n[STEP START] User enters a valid password and shows the password", flush=True)
    logger.info("[ACTION] Entering password 'Maya123@'...", flush=True)
    signup_page.enter_password("Maya123@")
    logger.info("[STEP END] User entered a valid password and showed the password", flush=True)


@step("User enters a mismatching confirm password and verifies the error message")
def enter_mismatch_confirm_password(signup_page: Signup):
    logger.info("\n[STEP START] User enters a mismatching password and verifies the error message", flush=True)

    logger.info("[ACTION] Entering mismatching confirm password 'Maya123'...", flush=True)
    signup_page.confirm_password("Maya123")

    logger.info("[ACTION/ASSERT] Verifying password mismatch error is displayed...", flush=True)
    signup_page.password_missmatch_error_displayed()
    time.sleep(10)

    logger.info("[STEP END] User verified mismatching confirm password error message", flush=True)


@step("User enters a valid confirm password and shows the password")
def enter_valid_confirm_password_and_show(signup_page: Signup):
    logger.info("\n[STEP START] User enters a valid confirm password and shows the password", flush=True)
    logger.info("[ACTION] Entering valid confirm password 'Maya123@'...", flush=True)
    signup_page.confirm_password("Maya123@")
    logger.info("[STEP END] User entered a valid confirm password and showed the password", flush=True)


@step("User hides the password and confirm password")
def hide_passwords(signup_page: Signup):
    logger.info("\n[STEP START] User hides the password and confirm password", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User hid the password and confirm password", flush=True)


@step("User verifies the SMS checkbox is only visible when a park with phone number is selected")
def verify_sms_checkbox_visibility(signup_page: Signup):
    logger.info("\n[STEP START] User verifies SMS checkbox visibility", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User verified SMS checkbox visibility", flush=True)


@step("User checks and unchecks the SMS option")
def toggle_sms_option(signup_page: Signup):
    logger.info("\n[STEP START] User checks and unchecks the SMS option", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User checked and unchecked SMS option", flush=True)


@step("User checks and unchecks the email option")
def toggle_email_option(signup_page: Signup):
    logger.info("\n[STEP START] User checks and unchecks the email option", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User checked and unchecked email option", flush=True)


@step("User clicks create account")
def click_create_account(signup_page: Signup):
    logger.info("\n[STEP START] User clicks create account", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User clicked create account", flush=True)


@step("User verifies the UI elements in the OTP bottom sheet")
def verify_otp_bottom_sheet_ui(signup_page: Signup):
    logger.info("\n[STEP START] User verifies the UI elements in the OTP bottom sheet", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User verified OTP bottom sheet UI elements", flush=True)


@step("User enters an invalid OTP and verifies the error message")
def enter_invalid_otp(signup_page: Signup):
    logger.info("\n[STEP START] User enters an invalid OTP and verifies the error message", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User entered invalid OTP and verified error message", flush=True)


@step("User clicks resend OTP and waits for 60 seconds")
def resend_otp_and_wait(signup_page: Signup):
    logger.info("\n[STEP START] User clicks resend OTP and waits for 60 seconds", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User clicked resend OTP and waited 60 seconds", flush=True)


@step("User enters a valid OTP and submits")
def enter_valid_otp(signup_page: Signup):
    logger.info("\n[STEP START] User enters a valid OTP and submits", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User entered valid OTP and submitted", flush=True)


@step("User verifies the success message and clicks login to your account")
def verify_success_and_login(signup_page: Signup):
    logger.info("\n[STEP START] User verifies success message and clicks login", flush=True)
    logger.info("[INFO] (Placeholder step - no action implemented)", flush=True)
    logger.info("[STEP END] User verified success message and clicked login", flush=True)