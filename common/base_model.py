from functools import cached_property

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pages
import time

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
