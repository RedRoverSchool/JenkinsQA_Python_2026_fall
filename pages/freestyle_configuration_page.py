from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.freestyle_project_page import FreestyleProjectPage


class FreestyleConfigurationPage(BasePage):
    def click_save(self) -> FreestyleProjectPage:
        from pages.freestyle_project_page import FreestyleProjectPage

        self.driver.find_element(By.NAME, "Submit").click()

        return FreestyleProjectPage(self.driver)
