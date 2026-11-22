from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.error_page import ErrorPage

class RenamePage(BasePage):
    NEW_NAME_INPUT = (By.NAME, "newName")
    RENAME_BUTTON = (By.NAME, "Submit")

    def submit_new_name(self, new_name):
        input_field = self.driver.find_element(*self.NEW_NAME_INPUT)
        input_field.clear()
        input_field.send_keys(new_name)
        self.driver.find_element(*self.RENAME_BUTTON).click()

    def rename_to(self, new_name, return_page_class=None):
        self.submit_new_name(new_name)
        if return_page_class:
            return return_page_class(self.driver)
        from pages.base_item_page import BaseItemPage
        return BaseItemPage(self.driver)

    def try_rename_to(self, invalid_name=""):
        self.submit_new_name(invalid_name)
        return ErrorPage(self.driver)