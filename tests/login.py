import time
import logging
from pytest_bdd import given, parsers, then, when

from page.home import Home
from page.login_page import Login


#scenarios("../features/login.feature")
import logging
logger = logging.getLogger(__name__)

# --- STEP 1 & 2: LAUNCH & NAVIGATE ---
@given("the user launches the app and navigates to the email screen")
def step_launch_and_navigate(driver, home_page: Home):
    assert driver is not None, "Driver instance was not properly initialized"

    # Handle sign-in navigation from Home if displayed
    if home_page.is_sign_in_button_displayed():
        logger.info("\n[INFO] Home screen loaded. Clicking Sign In / Create Account...")
        home_page.click_sign_in_create_account()
        time.sleep(3)  # Wait for transition/refresh to complete
    else:
        logger.info("\n[INFO] Already on email screen or Sign-In button not present.")


# --- STEP 3 & 4: EMAIL SCREEN UI & TEXT VERIFICATION ---
@when("the user verifies all email screen UI elements and text")
def step_verify_email_screen_ui_and_text(login_page: Login):
    logger.info("\n[INFO] Verifying Email Screen UI Elements & Text...")

    # Check visibility of UI components
    assert login_page.is_email_textbox_displayed(), "Email textbox is not displayed"
    assert login_page.is_guest_button_displayed(), "'Continue as Guest' button is not displayed"

    # Verify exact text values against expected UI copy
    actual_title = login_page.get_email_title_text()
    actual_subtitle = login_page.get_email_subtitle_text()

    expected_title = "Ready for Ride?"
    expected_subtitle = (
        "Enter your email to get started! If we find an account associated "
        "with your email, you’ll be prompted to enter your password. "
        "If no account exists, we’ll help you get started!"
    )

    logger.info(f"[DEBUG] Found Email Title: '{actual_title}'")
    logger.info(f"[DEBUG] Found Email Subtitle: '{actual_subtitle}'")

    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in '{actual_title}'"
    assert expected_subtitle in actual_subtitle, f"Expected subtitle '{expected_subtitle}' not found in '{actual_subtitle}'"


# --- STEP 5 & 6: INVALID EMAIL VALIDATION ---
@when(parsers.parse('the user enters an invalid email "{invalid_email}" and verifies the error message'))
def step_enter_invalid_email_and_verify(login_page: Login, invalid_email: str):
    logger.info(f"\n[INFO] Entering invalid email: '{invalid_email}' to test validation...")
    login_page.enter_email(invalid_email)

    assert login_page.is_email_error_displayed(), "Expected email validation error message was not displayed"

    # Validate exact error text
    actual_error = login_page.get_email_error_msg()
    expected_error = "Invalid email address."
    logger.info(f"[DEBUG] Found Email Error: '{actual_error}'")
    assert expected_error in actual_error, f"Expected error '{expected_error}' not found in '{actual_error}'"

    logger.info("[INFO] Email validation error successfully verified.")


# --- STEP 7: VALID EMAIL SUBMISSION ---
@when(parsers.parse('the user enters a valid email "{valid_email}" and submits'))
def step_enter_valid_email_and_submit(login_page: Login, valid_email: str):
    logger.info(f"\n[INFO] Entering valid email: '{valid_email}'...")
    login_page.enter_email(valid_email)
    login_page.click_email_submit()
    time.sleep(2)


# --- STEP 8: PASSWORD SCREEN UI & DISPLAYED EMAIL VERIFICATION ---
@then("the user verifies all password screen UI elements and displayed email")
def step_verify_password_screen_ui(login_page: Login):
    logger.info("\n[INFO] Verifying Password Screen UI Elements & Displayed Email...")

    assert login_page.verify_password_screen_loaded(), "Password screen title is not displayed"
    assert login_page.is_password_textbox_displayed(), "Password textbox is not displayed"
    assert login_page.is_forgot_password_displayed(), "'Forgot Password' button is not displayed"

    # Verify header & subtitle text
    actual_title = login_page.get_password_title_text()
    actual_subtitle = login_page.get_password_subtitle_text()

    expected_title = "Welcome Back!"
    expected_subtitle = "Enter Your Password to Continue."

    logger.info(f"[DEBUG] Found Password Title: '{actual_title}'")
    logger.info(f"[DEBUG] Found Password Subtitle: '{actual_subtitle}'")

    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in '{actual_title}'"
    assert expected_subtitle in actual_subtitle, f"Expected subtitle '{expected_subtitle}' not found in '{actual_subtitle}'"

    # Verify the email carried over matches the email entered previously
    displayed_email = login_page.get_displayed_email_text()
    expected_email = "thangavel@tuna.group"
    logger.info(f"[DEBUG] Displayed Email on Password Screen: '{displayed_email}'")
    assert expected_email in displayed_email, f"Expected email '{expected_email}' not found in '{displayed_email}'"


# --- STEP 9: INVALID PASSWORD VALIDATION ---
@when(parsers.parse('the user enters an invalid password "{invalid_password}" and verifies the error message'))
def step_enter_invalid_password_and_verify(login_page: Login, invalid_password: str):
    logger.info("\n[INFO] Testing invalid password submission...")
    login_page.enter_password(invalid_password)
    login_page.click_password_submit()

    assert login_page.is_password_error_displayed(), "Expected password error message was not displayed"

    # Validate exact error text
    actual_error = login_page.get_password_error_msg
    expected_error = "Incorrect username or password."
    logger.info(f"[DEBUG] Found Password Error: '{actual_error}'")
    assert expected_error in actual_error, f"Expected error '{expected_error}' not found in '{actual_error}'"

    logger.info("[INFO] Password validation error successfully verified.")


# --- STEP 10: VALID PASSWORD SUBMISSION ---
@when(parsers.parse('the user enters a valid password "{valid_password}" and submits'))
def step_enter_valid_password_and_submit(login_page: Login, valid_password: str):
    logger.info("\n[INFO] Entering valid password and logging in...")
    login_password = login_page.enter_password(valid_password)
    login_page.click_password_submit()
    time.sleep(5)  # Allow login processing and post-login refresh


# --- STEP 11: VERIFY HOME SCREEN WELCOME MESSAGE ---
@then("the user verifies the home screen is displayed via the manage account button")
def step_verify_home_screen_post_login(home_page: Home):
    logger.info("\n[INFO] Verifying home screen state via Manage Account button ...")

    assert home_page.is_manage_account_displayed(), "Home screen welcome indicator/search interface was not displayed post-login"
    logger.info("[SUCCESS] Full authentication flow executed and verified successfully!")