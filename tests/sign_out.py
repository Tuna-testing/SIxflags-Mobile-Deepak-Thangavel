from pytest_bdd import given, when, then

from page.home import Home
from page.login_page import Login
from page.more_page import More

#scenarios("../features/sign_out.feature")
import logging
logger = logging.getLogger(__name__)
@given("the user is logged into the application")
def user_is_logged_in(home_page: Home):
    logger.info("\n[INFO] Verifying home screen state via welcome indicator...")
    assert home_page.is_manage_account_displayed(), "Home screen welcome indicator/search interface was not displayed post-login"


@when("the user navigates to the More tab")
def navigate_to_more_tab(more_page: More):
    logger.info("\n[INFO] clicking on more tab...")
    more_page.click_more_tab()

@then("the More screen title should be displayed")
def verify_more_screen_title(more_page: More):
    logger.info("\n[INFO] Verifying More screen state via title indicator...")
    assert more_page.is_more_screen_title_displayed(), "More screen title is not displayed"


@when("the user scrolls to the bottom of the More screen")
def scroll_to_bottom_of_more_screen(more_page: More):
    logger.info("\n[INFO] scroll down to see the Sign out button...")
    pass

@when("the user clicks on Sign Out")
def click_sign_out_button(more_page: More):
    logger.info("\n[INFO] clicking on sign out button...")
    more_page.click_sign_out()
    more_page.cancel_sign_out()

@when("the user cancels the sign out confirmation")
def cancel_sign_out_prompt(more_page: More):
    logger.info("\n[INFO] cancel the sign out confirmation...")
    pass


@then("the More screen should still be displayed")
def verify_user_remains_on_more_screen(more_page: More):
    logger.info("\n[INFO] Verifying More screen state via app version indicator...")
    assert (more_page.is_app_version_displayed()), "User was logged out unexpectedly after clicking 'No'"


@when("the user confirms the sign out action")
def confirm_sign_out_prompt(more_page: More):
    logger.info("\n[INFO] confirming the sign out confirmation...")

    more_page.click_sign_out()
    more_page.confirm_sign_out()

@then("the Enter Email screen should be displayed")
def verify_enter_email_screen_visible(login_page: Login):
    logger.info("\n[INFO] Verifying Enter email screen state via screen title...")

    actual_title = login_page.get_email_title_text()
    expected_title = "Ready for Ride?"
    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in '{actual_title}'"

