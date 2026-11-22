from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.freestyle_configuration_page import FreestyleConfigurationPage


class FreestyleProjectPage(BasePage):
    DESCRIPTION = (By.ID, "description")

    def click_configuration(self) -> FreestyleConfigurationPage:
        self.driver.find_element(By.XPATH, "//a[contains(., 'Configure')]").click()

        return FreestyleConfigurationPage(self.driver)

    def get_description(self) -> str:
        return self.wait10.until(
            EC.visibility_of_element_located(self.DESCRIPTION)
        ).text

    def is_project_disabled(self) -> bool:
        return self.wait10.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"), "This project is currently disabled"
            )
        )

    def is_enable_button_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")
            )
        ).is_displayed()

    def enable_project(self) -> FreestyleProjectPage:
        enable_locator = (By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")
        self.wait10.until(EC.element_to_be_clickable(enable_locator)).click()

        return self

    def is_project_enabled(self) -> bool | WebElement:
        return self.wait10.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'This project is currently disabled')]")
            )
        )

    def is_enable_button_hidden(self) -> bool | WebElement:
        return self.wait10.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")
            )
        )