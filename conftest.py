# conftest.py
import os
import shutil

# Tell pytest to load all modular fixtures and hooks automatically
pytest_plugins = [
    "fixtures.driver",
    "fixtures.pages",
    "hooks.bdd_hooks",
    "hooks.html_hooks",
    "hooks.report_hooks",
    "fixtures.api",
]


def pytest_sessionstart(session):
    """Clear allure report/results before test session starts."""
    for folder in ["reports/allure-report", "reports/allure-results"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted {folder}")
        os.makedirs(folder, exist_ok=True)




def pytest_addoption(parser):
    """Adds CLI flags for target platform and environment."""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Target platform: android or ios",
    )
    parser.addoption(
        "--env",
        action="store",
        default="prod",
        choices=["uat", "prod"],
        help="Target execution environment: uat, or prod",
    )



