from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.freestyle_project_page import FreestyleProjectPage


class FreestyleConfigurationPage(BasePage):
    ENVIRONMENT_BUTTON = (
        By.XPATH,
        "//button[.//span[normalize-space()='Environment']]"
    )
    ENVIRONMENT_OPTIONS = [
        (By.ID, "cb18"),
        (By.ID, "cb19"),
        (By.ID, "cb21"),
        (By.ID, "cb22"),
        (By.ID, "cb23"),
        (By.NAME, "hudson-tasks-AntWrapper"),
    ]

    def click_environment(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.ENVIRONMENT_BUTTON)
        ).click()

        return self

    def are_environment_options_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.ENVIRONMENT_OPTIONS
        )

    def are_environment_options_unselected(self) -> bool:
        return all(
            not self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_selected()
            for locator in self.ENVIRONMENT_OPTIONS
        )

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