from appium.webdriver.common.appiumby import AppiumBy


class W3CGesture:
    @staticmethod
    def tap(driver, element):
        driver.execute_script('mobile: clickGesture', {
            'elementId': element.id
        })

    @staticmethod
    def scroll_up(driver):
        driver.execute_script('mobile: scrollGesture', {
            'left': 100, 'top': 100, 'width': 600, 'height': 600,
            'direction': 'up',
            'percent': 3.0
        })

    @staticmethod
    def scroll_down(driver):
        driver.execute_script('mobile: scrollGesture', {
            'left': 100, 'top': 100, 'width': 600, 'height': 600,
            'direction': 'down',
            'percent': 3.0
        })

    @staticmethod
    def swipe_left(driver):
        driver.execute_script('mobile: swipeGesture', {
            'left': 100, 'top': 100, 'width': 600, 'height': 600,
            'direction': 'left',
            'percent': 0.75
        })

    @staticmethod
    def swipe_right(driver):
        driver.execute_script('mobile: swipeGesture', {
            'left': 100, 'top': 100, 'width': 600, 'height': 600,
            'direction': 'right',
            'percent': 0.75
        })

    @staticmethod
    def scroll_to_element(driver, by, value):
        driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value=f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().{by}("{value}"))'
        )
