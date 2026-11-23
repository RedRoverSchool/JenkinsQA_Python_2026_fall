from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.rename_page import RenamePage

class BaseItemPage(BasePage):
    HEADLINE_NAME = (By.XPATH, "//h1[contains(@class,'job-index-headline')]")
    RENAME_LINK = (By.XPATH, "//a[contains(@href,'/confirm-rename')]")
    DELETE_LINK = (By.XPATH, "//a[@data-title='Delete Multibranch Pipeline']")

    def get_item_name(self) -> str:
        return self.driver.find_element(*self.HEADLINE_NAME).text

    def click_rename(self) -> RenamePage:
        self.driver.find_element(*self.RENAME_LINK).click()
        return RenamePage(self.driver)

    def click_delete(self):
        self.driver.find_element(*self.DELETE_LINK).click()
        return self
