# hooks/report_hooks.py
import os
import shutil


def pytest_sessionstart(session):
    """Triggers at the start of the test session to wipe previous Allure reports."""
    for folder in ["reports/allure-report", "reports/allure-results"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted {folder}")
        os.makedirs(folder, exist_ok=True)