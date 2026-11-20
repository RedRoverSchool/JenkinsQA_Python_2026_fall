from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.freestyle_project_page import FreestyleProjectPage


class FreestyleConfigurationPage(BasePage):
    def click_save(self) -> FreestyleProjectPage:
        from pages.freestyle_project_page import FreestyleProjectPage

        self.driver.find_element(By.NAME, "Submit").click()
        self.wait10.until(EC.presence_of_element_located((By.ID, "description-link")))

        return FreestyleProjectPage(self.driver)

    def is_enable_disable_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located((By.ID, "enable-disable-project"))
        ).is_selected()

    def is_enable_disable_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located((By.ID, "enable-disable-project"))
        ).is_displayed()

    def disable_project(self) -> FreestyleConfigurationPage:
        self.driver.find_element(
            By.CSS_SELECTOR, "label[for='enable-disable-project']"
        ).click()

        return self