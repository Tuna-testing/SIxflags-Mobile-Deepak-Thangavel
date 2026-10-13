#utills/desired_cap.py

import os
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from utils import AppiumServerManager


class CapabilitiesBuilder:
    APP_IDENTIFIERS = {
        "android": {
            "uat": "com.sixflags.android.uat",
            "prod": "com.sixflags.android"
        },
        "ios": {
            "uat": "com.sixflags.ios.uat",
            "prod": "com.sixflags.ios"
        }
    }

    @staticmethod
    def _get_worker_index():
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
        if worker_id.startswith("gw"):
            return int(worker_id[2:])
        return 0

    @classmethod
    def android(cls, env: str = "prod") -> UiAutomator2Options:
        worker_index = CapabilitiesBuilder._get_worker_index()
        system_port = AppiumServerManager.get_free_system_port()
        target_package = cls.APP_IDENTIFIERS["android"].get(env.lower(), cls.APP_IDENTIFIERS["android"]["prod"])

        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("appium:automationName", "UiAutomator2")         
        options.set_capability("appium:udid", "43160DLJH0007L")
        options.set_capability("appium:systemPort", system_port)

        # sensible defaults for the project (can be overridden)
        options.set_capability("appium:appPackage", target_package)
        options.set_capability("appium:appActivity", "com.sixflags.android.MainActivity")
        options.set_capability("appium:appWaitActivity", "*")

        options.set_capability("appium:autoGrantPermissions", True)
        options.set_capability("appium:ignoreHiddenApiPolicyError", True)
        options.set_capability("appium:noReset", True)
        options.set_capability("appium:fullReset", False)
        options.set_capability("appium:forceAppLaunch", True)
        options.set_capability("appium:shouldTerminateApp", True)
        options.set_capability("appium:enforceXPath1", True)
        """options.set_capability("appium:userProfile", 1)"""

        return options

    @classmethod
    def ios(cls, env: str = "prod") -> XCUITestOptions:
        worker_index = CapabilitiesBuilder._get_worker_index()
        wda_local_port = 8100 + worker_index
        target_bundle_id = cls.APP_IDENTIFIERS["ios"].get(env.lower(), cls.APP_IDENTIFIERS["ios"]["prod"])

        options = XCUITestOptions()
        options.set_capability("platformName", "iOS")
        options.set_capability("appium:automationName", "XCUITest")
        options.set_capability("appium:deviceName", "iPhone")
        options.set_capability("appium:udid", "00008110-000854660121401E")
        options.set_capability("appium:bundleId", target_bundle_id)
        options.set_capability("appium:wdaLocalPort", wda_local_port)
        options.set_capability("appium:autoAcceptAlerts", True)
        options.set_capability("appium:noReset", True)

        # Required for physical device signing
        options.set_capability("appium:xcodeOrgId", "24295WXK2R")  # 10-character Apple Team ID
        options.set_capability("appium:xcodeSigningId", "iPhone Developer")
        options.set_capability("appium:autoAcceptAlerts", True)
        options.set_capability("appium:maxTypingFrequency", 15)

        return options
