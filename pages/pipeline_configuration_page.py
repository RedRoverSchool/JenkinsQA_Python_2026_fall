from __future__ import annotations
from typing import TYPE_CHECKING, Self
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.pipeline_page import PipelinePage


class PipelineConfigurationPage(BasePage):
    DESCRIPTION_FLD = (By.XPATH, "//textarea[@name='description']")

    def click_save(self) -> PipelinePage:
        from pages.pipeline_page import PipelinePage

        self.driver.find_element(By.NAME, "Submit").click()

        return PipelinePage(self.driver)

    def switch_button_disabled(self) -> Self:
        self.driver.find_element(By.CSS_SELECTOR, "[class = 'jenkins-toggle-switch__label ']").click()

        return self

    def enter_description(self, text: str) -> "PipelineConfigurationPage":
        self.wait10.until(EC.url_contains(text))
        self.wait10.until(EC.url_contains("configure"))
        desc = self.driver.find_element(*self.DESCRIPTION_FLD)
        desc.click()
        desc.clear()
        desc.send_keys(text)
        return self

    def get_description_value(self):
        desc = self.driver.find_element(*self.DESCRIPTION_FLD)
        return desc.get_attribute("value")
