from __future__ import annotations
from typing import TYPE_CHECKING
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


if TYPE_CHECKING:
    from pages.multiconfiguration_project_page import MulticonfigurationProjectPage


class MulticonfigurationConfigurationPage(BasePage):

    def enter_description(self, description) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "description").send_keys(description)
        return MulticonfigurationConfigurationPage(self.driver)

    def enable_discard_old_builds(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.XPATH, "//label[contains(., 'Discard old builds')]").click()
        return self

    def set_days_to_keep(self, days_to_keep: int) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "_.daysToKeepStr").send_keys(days_to_keep)
        return self

    def set_builds_to_keep(self, builds_to_keep: int) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "_.numToKeepStr").send_keys(builds_to_keep)
        return self

    def click_save(self) -> MulticonfigurationProjectPage:
        from pages.multiconfiguration_project_page import MulticonfigurationProjectPage
        self.driver.find_element(By.NAME, "Submit").click()

        return MulticonfigurationProjectPage(self.driver)

    def get_days_to_keep(self) -> str:
        return self.driver.find_element(By.NAME, "_.daysToKeepStr").get_attribute("value")

    def get_builds_to_keep(self) -> str:
        return self.driver.find_element(By.NAME, "_.numToKeepStr").get_attribute("value")

    def is_discard_old_builds_enabled(self) -> bool:
        return self.driver.find_element(By.ID, "cb2").is_selected()

    def enable_github_project(self) -> MulticonfigurationConfigurationPage:
        github_checkbox = self.driver.find_element(By.XPATH, "//label[contains(., 'GitHub project')]")
        self.driver.execute_script("arguments[0].scrollIntoView();",github_checkbox)
        github_checkbox.click()
        return self

    def enter_project_url(self, project_url: str) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "_.projectUrlStr").send_keys(project_url)
        return self

    def get_project_url(self) -> str:
        return self.driver.find_element(By.NAME, "_.projectUrlStr").get_attribute("value")

    def is_github_project_enabled(self) -> bool:
        return self.driver.find_element(By.ID, "cb3").is_selected()

    def enable_this_project_is_parameterised(self) -> MulticonfigurationConfigurationPage:
        this_project_is_parameterised_checkbox = self.driver.find_element(By.XPATH, "//input[@id='cb4']/following-sibling::label")
        self.driver.execute_script( "arguments[0].scrollIntoView({block: 'center'});", this_project_is_parameterised_checkbox)
        this_project_is_parameterised_checkbox.click()
        return self

    def click_add_parameter(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.CSS_SELECTOR, '[suffix="parameterDefinitions"]').click()
        return self

    def select_string_parameter(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.XPATH, "//button[normalize-space()='String Parameter']").click()
        return self

    def set_parameter_name(self, parameter_name: str) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "parameter.name").send_keys(parameter_name)
        return self

    def set_default_value(self, default_value: str) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "parameter.defaultValue").send_keys(default_value)
        return self

    def set_parameter_description(self, parameter_description: str) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.NAME, "parameter.description").send_keys(parameter_description)
        return self

    def is_this_project_parameterised_enabled(self) -> bool:
        return self.driver.find_element(By.ID, "cb4").is_selected()

    def get_parameter_name(self) -> str:
        return self.driver.find_element(By.NAME, "parameter.name").get_attribute("value")

    def get_default_value(self) -> str:
        return self.driver.find_element(By.NAME, "parameter.defaultValue").get_attribute("value")

    def get_parameter_description(self) -> str:
        return self.driver.find_element(By.NAME, "parameter.description").get_attribute("value")

    def click_preview(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.XPATH, "//a[text()='Preview']").click()
        return self

    def is_preview_displayed(self) -> bool:
        self.wait5.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'textarea-preview')]")
            )
        )
        return self.driver.find_element(By.XPATH, "//div[contains(@class, 'textarea-preview')]").is_displayed()

    def click_hide_preview(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.XPATH, "//a[text()='Hide preview']").click()
        return self

    def is_preview_hidden(self) -> bool:
        return self.driver.find_element(By.XPATH,"//a[text()='Preview']").is_displayed()

