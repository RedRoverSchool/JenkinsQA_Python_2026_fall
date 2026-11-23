from __future__ import annotations
from typing import TYPE_CHECKING
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


if TYPE_CHECKING:
    from pages.multiconfiguration_project_page import MulticonfigurationProjectPage


class MulticonfigurationConfigurationPage(BasePage):

    def enter_description_and_click_save(self, description) -> MulticonfigurationProjectPage:
        from pages.multiconfiguration_project_page import MulticonfigurationProjectPage

        self.driver.find_element(By.NAME, "description").send_keys(description)
        self.driver.find_element(By.NAME, "Submit").click()

        return MulticonfigurationProjectPage(self.driver)

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

