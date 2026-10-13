# fixtures/driver.py
import os

import pytest

from utils.driver_manager import DriverFactory


@pytest.fixture(scope="session")
def platform(request):
    """Determines target platform from CLI option or test markers (@pytest.mark.ios / @pytest.mark.android)."""
    cli_platform = request.config.getoption("--platform")
    if cli_platform:
        return cli_platform.lower()
    if request.node.get_closest_marker("ios"):
        return "ios"
    if request.node.get_closest_marker("android"):
        return "android"

    # Default fallback if no marker or CLI arg is specified
    return "android"


@pytest.fixture(scope="session")
def driver(platform, env,request):
    """Starts Appium server, initializes driver instance, binds it to test node, and handles teardown."""
    os.makedirs("logs", exist_ok=True)

    # 1. DriverFactory handles starting Appium server + loading capabilities + connecting Remote driver
    driver_instance = DriverFactory.init_driver(platform=platform, env=env)
    driver_instance.implicitly_wait(30)

    # 2. Attach driver to pytest node so bdd_hooks.py can capture screenshots on failure/step completion
    request.node.driver = driver_instance

    yield driver_instance

    # 3. DriverFactory quits driver AND stops the worker's Appium server
    DriverFactory.quit_driver()

@pytest.fixture(scope="session")
def env(request):
    """Reads the --env CLI option."""
    return request.config.getoption("--env", default="prod").lower()

