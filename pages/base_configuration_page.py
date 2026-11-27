from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class BaseConfigurationPage(BasePage):
    SAVE_BTN = (By.XPATH, "//button[@name='Submit']")
    APPLY_BTN = (By.XPATH, "//button[@name='Apply']")
    GENERAL_SECTION = (By.XPATH, "//button[contains(@class,'task-link')][.//span[normalize-space()='General']]")

    def click_save(self) -> Self:
        self.driver.find_element(*self.SAVE_BTN).click()
        from pages.base_item_page import BaseItemPage
        return BaseItemPage(self.driver)

    def click_apply(self) -> Self:
        self.driver.find_element(*self.APPLY_BTN).click()
        return self

    def is_general_section_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.GENERAL_SECTION)
        ).is_displayed()
