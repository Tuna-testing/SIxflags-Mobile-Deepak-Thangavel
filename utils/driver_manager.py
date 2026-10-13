#utills/driver_manager.py

import os
from appium import webdriver
from .desired_cap import CapabilitiesBuilder
from .appium_server import AppiumServerManager


class DriverFactory:
    _worker_drivers = {}
    _worker_services = {}

    @staticmethod
    def _get_worker_id():
        return os.environ.get("PYTEST_XDIST_WORKER", "master")

    @staticmethod
    def init_driver(platform, env="prod", appium_port=None):
        worker_id = DriverFactory._get_worker_id()

        url, service = AppiumServerManager.start(port=appium_port, worker_id=worker_id)
        DriverFactory._worker_services[worker_id] = service

        if platform == "android":
            options = CapabilitiesBuilder.android(env=env)
        elif platform == "ios":
            options = CapabilitiesBuilder.ios(env=env)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        driver = webdriver.Remote(url, options=options)
        DriverFactory._worker_drivers[worker_id] = driver
        return driver

    @staticmethod
    def quit_driver():
        worker_id = DriverFactory._get_worker_id()

        driver = DriverFactory._worker_drivers.get(worker_id)
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
            DriverFactory._worker_drivers[worker_id] = None

        service = DriverFactory._worker_services.get(worker_id)
        if service:
            try:
                AppiumServerManager.stop(service)
            except Exception:
                pass
            DriverFactory._worker_services[worker_id] = None
