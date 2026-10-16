from unittest import skip

import pytest
from pytest_bdd import scenario


@pytest.mark.smoke
@pytest.mark.ios
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="auth_flow")
@scenario('../features/login.feature', 'Login flow')
def test_01_login_scenarios():
    pass

@pytest.mark.skip(reason="Skipping sign-up scenarios due to known issues.")
@pytest.mark.smoke
@pytest.mark.ios
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="auth_flow")
@scenario('../features/sign_out.feature', 'sign out flow')
def test_02_sign_out_scenarios():
    pass

@pytest.mark.skip(reason="Skipping sign-up scenarios due to known issues.")
@pytest.mark.smoke
@pytest.mark.ios
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="auth_flow")
@scenario('../features/signup.feature', 'regression sign up flow')
def test_03_sign_up_scenarios():
    pass


