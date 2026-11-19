from functools import cached_property

from selenium.webdriver.support.ui import WebDriverWait

class BaseModel:

    def __init__(self, driver):
        self.driver = driver

    @cached_property
    def wait2(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 2)

    @cached_property
    def wait5(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 5)

    @cached_property
    def wait10(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 10)
