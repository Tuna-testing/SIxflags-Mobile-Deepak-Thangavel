import time
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.common.exceptions import NoSuchElementException


class Gesture:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        size = driver.get_window_size()
        self.width = size['width']
        self.height = size['height']

    def tap(self, element):
        loc, size = element.location, element.size
        x = int(loc['x'] + size['width'] / 2)
        y = int(loc['y'] + size['height'] / 2)

        actions = ActionBuilder(self.driver, mouse=PointerInput(POINTER_TOUCH, "touch"))
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.1)
        actions.pointer_action.release()
        actions.perform()

    def _swipe(self, start_x, start_y, end_x, end_y, duration_ms=600):
        actions = ActionBuilder(self.driver, mouse=PointerInput(POINTER_TOUCH, "touch"))
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000.0)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    def swipe_left(self, duration_ms=600):
        self._swipe(int(self.width * 0.85), int(self.height * 0.5),
                    int(self.width * 0.15), int(self.height * 0.5), duration_ms)

    def swipe_right(self, duration_ms=600):
        self._swipe(int(self.width * 0.15), int(self.height * 0.5),
                    int(self.width * 0.85), int(self.height * 0.5), duration_ms)

    def scroll_down(self, duration_ms=600):
        self._swipe(int(self.width * 0.5), int(self.height * 0.8),
                    int(self.width * 0.5), int(self.height * 0.2), duration_ms)

    def scroll_up(self, duration_ms=600):
        self._swipe(int(self.width * 0.5), int(self.height * 0.2),
                    int(self.width * 0.5), int(self.height * 0.8), duration_ms)

    def scroll_to_element(self, locator: tuple, max_scrolls: int = 10) -> bool:
        max_scrolls = int(max_scrolls)
        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    return True
            except NoSuchElementException:
                self.scroll_down(duration_ms=800)
        raise NoSuchElementException(
            f"Element {locator} not found after {max_scrolls} scrolls."
        )

    def scroll_to_bottom(self, max_swipes: int = 10):
        prev_source = ""
        for _ in range(int(max_swipes)):
            curr_source = self.driver.page_source
            if curr_source == prev_source:
                break
            prev_source = curr_source
            self.scroll_down()
            time.sleep(0.5)

    def scroll_to_top(self, max_swipes: int = 10):
        prev_source = ""
        for _ in range(int(max_swipes)):
            curr_source = self.driver.page_source
            if curr_source == prev_source:
                break
            prev_source = curr_source
            self.scroll_up()
            time.sleep(0.5)

    def drag_and_drop(self, source_element, target_element, hold_ms: int = 300):
        src_loc, src_size = source_element.location, source_element.size
        start_x = int(src_loc['x'] + src_size['width'] / 2)
        start_y = int(src_loc['y'] + src_size['height'] / 2)

        tgt_loc, tgt_size = target_element.location, target_element.size
        end_x = int(tgt_loc['x'] + tgt_size['width'] / 2)
        end_y = int(tgt_loc['y'] + tgt_size['height'] / 2)

        touch = PointerInput(POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=touch)

        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(hold_ms / 1000.0)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.pointer_up()

        actions.perform()

    def scroll_element_down(self, element, factor=0.5, duration_ms=600):
        loc = element.location
        size = element.size
        start_x = loc['x'] + size['width'] // 2
        start_y = loc['y'] + size['height'] // 2
        end_y = int(start_y + size['height'] * 0.5)
        self.driver.swipe(start_x, start_y, start_x, end_y, 600)

    def scroll_element_up(self, element, factor=0.5, duration_ms=600):
        loc = element.location
        size = element.size
        start_x = loc['x'] + size['width'] // 2
        start_y = loc['y'] + size['height'] // 2
        end_y = int(start_y - size['height'] * 0.5)
        self.driver.swipe(start_x, start_y, start_x, end_y, 600)
