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

    SCM_BUTTON = (
        By.XPATH,
        "//button[.//span[normalize-space()='Source Code Management']]"
    )
    SCM_OPTIONS = [
        (By.CSS_SELECTOR, "label[for='radio-block-0']"),
        (By.CSS_SELECTOR, "label[for='radio-block-1']"),
    ]
    GIT_OPTION = (By.CSS_SELECTOR, "label[for='radio-block-1']")
    GIT_FIELDS = [
        (By.CSS_SELECTOR, "input[name='_.url']"),
        (By.CSS_SELECTOR, "select[name='_.credentialsId']"),
        (By.CSS_SELECTOR, "input[name='_.name'][default='*/master']"),
    ]
    REPOSITORY_URL = (By.CSS_SELECTOR, "input[name='_.url']")
    GIT_ERROR_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"
    )

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

    def click_scm(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.SCM_BUTTON)
        ).click()

        return self

    def are_scm_options_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.SCM_OPTIONS
        )

    def is_none_scm_selected(self) -> bool:
        return self.wait10.until(
            EC.presence_of_element_located((By.ID, "radio-block-0"))
        ).is_selected()

    def select_git_scm(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.GIT_OPTION)
        ).click()

        return self

    def are_git_fields_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.GIT_FIELDS
        )

    def enter_repository_url(self, repository_url: str) -> FreestyleConfigurationPage:
        url_field = self.wait10.until(
            EC.visibility_of_element_located(self.REPOSITORY_URL)
        )
        url_field.send_keys(repository_url)
        url_field.send_keys("\t")

        return self

    def is_git_error_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.GIT_ERROR_MESSAGE)
        ).is_displayed()

    def click_save(self) -> FreestyleProjectPage:
        from pages.freestyle_project_page import FreestyleProjectPage

        self.driver.find_element(By.NAME, "Submit").click()
        self.wait10.until(
            EC.presence_of_element_located((By.ID, "description-link"))
        )

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