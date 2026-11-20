from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

if TYPE_CHECKING:
    from pages.pipeline_status_page import PipelineStatusPage

class PipelineConfigurationPage(BasePage):
    def click_save(self) -> PipelineStatusPage:
        from pages.pipeline_status_page import PipelineStatusPage

        self.driver.find_element(By.NAME, "Submit").click()

        # wait new page
        self.wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$=configure]")))

        return PipelineStatusPage(self.driver)

    class ClickOnLeftSideSection(Enum):
        GENERAL = "General"
        TRIGGERS = "Triggers"
        PIPELINE = "Pipeline"
        ADVANCED = "Advanced"

    def click_on_left_side_section(self,
                                   section: PipelineConfigurationPage.ClickOnLeftSideSection) -> PipelineConfigurationPage:
        self.wait2.until(EC.element_to_be_clickable((
            By.XPATH, f"//span[contains(text(),'{section.value}')]/ancestor::button"
        ))).click()

        return self

    def open_advanced_dropdown(self) -> PipelineConfigurationPage:
        self.wait2.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".jenkins-bottom-app-bar__shadow--stuck")))
        self.driver.find_element(By.CSS_SELECTOR, ".jenkins-section button.advancedButton").click()

        return self

    def set_quiet_period(self, seconds) -> PipelineConfigurationPage:
        self.wait2.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='hasCustomQuietPeriod'] + label"))).click()
        quiet_period_seconds = self.driver.find_element(By.CSS_SELECTOR, "input[name='quiet_period']")
        quiet_period_seconds.clear()
        quiet_period_seconds.send_keys(seconds, Keys.TAB)

        return self

    def get_quiet_period(self) -> str:
        return self.driver.find_element(By.CSS_SELECTOR, "input[name='quiet_period']").get_property("value")

    def get_quiet_period_error(self) -> str:
        return self.wait2.until(EC.visibility_of_element_located((
            By.XPATH,
            "//input[@name='quiet_period']/ancestor::div[contains(@class,'jenkins-form-item')]/descendant::div[@class='error']"
        ))).text
