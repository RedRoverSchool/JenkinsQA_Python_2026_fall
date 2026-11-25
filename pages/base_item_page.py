from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.rename_page import RenamePage
    from pages.base_configuration_page import BaseConfigurationPage

class BaseItemPage(BasePage):
    HEADLINE_NAME = (By.XPATH, "//h1[contains(@class,'job-index-headline')]")
    CONFIGURE_LINK = (By.XPATH, "//a[contains(@href,'/configure') and contains(@class,'task-link')]")
    RENAME_LINK = (By.XPATH, "//a[contains(@href,'/confirm-rename')]")
    DELETE_LINK = (By.XPATH, "//a[@data-title='Delete Multibranch Pipeline']")

    def get_item_name(self) -> str:
        return self.driver.find_element(*self.HEADLINE_NAME).text

    def click_configure(self, config_page_class=None):
        self.driver.find_element(*self.CONFIGURE_LINK).click()
        if config_page_class:
            return config_page_class(self.driver)
        from pages.base_configuration_page import BaseConfigurationPage
        return BaseConfigurationPage(self.driver)

    def click_rename(self) -> RenamePage:
        self.driver.find_element(*self.RENAME_LINK).click()
        from pages.rename_page import RenamePage
        return RenamePage(self.driver)

    def click_delete(self):
        self.driver.find_element(*self.DELETE_LINK).click()
        return self
