from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FolderConfigurationPage(BasePage):
    def set_display_name(self, display_name: str) -> Self:
        self.driver.find_element(By.NAME, "_.displayNameOrNull").send_keys(display_name)

        return self

    def click_apply(self) -> Self:
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()

        return self
