from __future__ import annotations
from enum import Enum
from selenium.webdriver import Keys
from typing import TYPE_CHECKING, Self
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

if TYPE_CHECKING:
    from pages.pipeline_page import PipelinePage


class PipelineConfigurationPage(BasePage):
    DESCRIPTION_FLD = (By.XPATH, "//textarea[@name='description']")

    TRIGGERS_TITLE = (By.XPATH, "//div[contains(@class, 'jenkins-section__title') and normalize-space()='Triggers']")

    REVERSE_BUILD_TRIGGER_CHECKBOX = (By.CSS_SELECTOR, "input[name='jenkins-triggers-ReverseBuildTrigger']")
    TIMER_TRIGGER_CHECKBOX = (By.CSS_SELECTOR, "input[name='hudson-triggers-TimerTrigger']")
    GITHUB_PUSH_TRIGGER_CHECKBOX = (By.CSS_SELECTOR, "input[name='com-cloudbees-jenkins-GitHubPushTrigger']")
    SCM_TRIGGER_CHECKBOX = (By.CSS_SELECTOR, "input[name='hudson-triggers-SCMTrigger']")
    REMOTE_TRIGGER_CHECKBOX = (By.CSS_SELECTOR, "input[name='pseudoRemoteTrigger']")

    REVERSE_BUILD_TRIGGER_HELP = (By.CSS_SELECTOR, "a[helpURL='/descriptor/jenkins.triggers.ReverseBuildTrigger/help']")
    TIMER_TRIGGER_HELP = (By.CSS_SELECTOR, "a[helpURL='/descriptor/hudson.triggers.TimerTrigger/help']")
    GITHUB_PUSH_TRIGGER_HELP = (By.CSS_SELECTOR,
                                "a[helpURL='/descriptor/com.cloudbees.jenkins.GitHubPushTrigger/help']")
    SCM_TRIGGER_HELP = (By.CSS_SELECTOR, "a[helpURL='/descriptor/hudson.triggers.SCMTrigger/help']")
    REMOTE_TRIGGER_HELP = (By.CSS_SELECTOR, "a[helpURL='/help/project-config/triggerRemotely.html']")


    def click_save(self) -> PipelinePage:
        from pages.pipeline_page import PipelinePage

        self.driver.find_element(By.NAME, "Submit").click()

        # wait new page
        self.wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$=configure]")))

        return PipelinePage(self.driver)

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

    def switch_button_disabled(self) -> Self:
        self.driver.find_element(By.CSS_SELECTOR, "[class = 'jenkins-toggle-switch__label ']").click()

        return self

    def get_description_value(self):
        desc = self.driver.find_element(*self.DESCRIPTION_FLD)
        return desc.get_attribute("value")

    def is_configuration_page_opened(self, item_name: str) -> bool:
        return f"/job/{item_name}/configure" in self.driver.current_url

    def get_triggers_title(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located(self.TRIGGERS_TITLE)).text

    def are_triggers_checkboxes_and_help_icons_displayed(self) -> bool:
        trigger_pairs = [
            (self.REVERSE_BUILD_TRIGGER_CHECKBOX, self.REVERSE_BUILD_TRIGGER_HELP),
            (self.TIMER_TRIGGER_CHECKBOX, self.TIMER_TRIGGER_HELP),
            (self.GITHUB_PUSH_TRIGGER_CHECKBOX, self.GITHUB_PUSH_TRIGGER_HELP),
            (self.SCM_TRIGGER_CHECKBOX, self.SCM_TRIGGER_HELP),
            (self.REMOTE_TRIGGER_CHECKBOX, self.REMOTE_TRIGGER_HELP),
        ]
        for checkbox_loc, help_loc in trigger_pairs:
            checkbox = self.wait5.until(EC.visibility_of_element_located(checkbox_loc))
            help_icon = self.wait5.until(EC.visibility_of_element_located(help_loc))
            if not (checkbox.is_displayed() and help_icon.is_displayed() and help_icon.text.strip() == "?"):
                return False
        return True