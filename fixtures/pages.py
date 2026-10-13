# fixtures/pages.py
import pytest
from page.home import Home
from page.login_page import Login
from page.more_page import More
from page.sign_up import Signup


@pytest.fixture
def login_page(driver):
    return Login(driver)


@pytest.fixture
def home_page(driver):
    return Home(driver)


@pytest.fixture
def more_page(driver):
    return More(driver)

@pytest.fixture
def signup_page(driver):
    return Signup(driver)



