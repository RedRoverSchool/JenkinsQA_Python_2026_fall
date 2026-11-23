from __future__ import annotations
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.folder_configuration_page import FolderConfigurationPage
from pages.freestyle_configuration_page import FreestyleConfigurationPage
from pages.multiconfiguration_configuration_page import MulticonfigurationConfigurationPage
from pages.pipeline_configuration_page import PipelineConfigurationPage
from pages.multibranch_configuration_page import MultibranchConfigurationPage
from pages.error_page import ErrorPage

class NewItemPage(BasePage):
    MULTIBRANCH = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    OK_BUTTON = (By.ID, "ok-button")
    SIDE_PANEL = (By.ID, "side-panel")
    ITEMS_TYPE_LIST = (By.ID, "items")
    PIPELINE_ITEM = (By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob",)

    def set_item_name(self, name: str) -> Self:
        self.wait10.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys(name)

        return self

    def get_item_name(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "name"))).get_attribute("value")

    def select_freestyle_and_click_ok(self) -> FreestyleConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "hudson_model_FreeStyleProject").click()
        self.wait2.until(EC.element_to_be_clickable((By.ID, "ok-button"))).click()

        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return FreestyleConfigurationPage(self.driver)

    def select_folder_and_click_ok(self) -> FolderConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "com_cloudbees_hudson_plugins_folder_Folder").click()
        self.driver.find_element(By.ID, "ok-button").click()

        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return FolderConfigurationPage(self.driver)

    def select_multiconfiguration_and_click_ok(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "hudson_matrix_MatrixProject").click()
        self.wait5.until(EC.element_to_be_clickable((By.ID, "ok-button")))
        self.driver.find_element(By.ID, "ok-button").click()

        return MulticonfigurationConfigurationPage(self.driver)


    def select_pipeline_and_click_ok(self) -> PipelineConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob").click()
        self.wait2.until(EC.element_to_be_clickable((By.ID, "ok-button"))).click()

        # wait new page
        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return PipelineConfigurationPage(self.driver)

    def select_multibranch_and_click_ok(self) -> MultibranchConfigurationPage:
        multibranch_option = self.wait5.until(
            EC.element_to_be_clickable(self.MULTIBRANCH)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", multibranch_option)
        multibranch_option.click()
        self.driver.find_element(*self.OK_BUTTON).click()
        self.wait5.until(
            EC.visibility_of_element_located(self.SIDE_PANEL)
        )

        return MultibranchConfigurationPage(self.driver)

    def select_multibranch(self) :
        multibranch_option = self.wait5.until(
            EC.element_to_be_clickable(self.MULTIBRANCH)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", multibranch_option)
        multibranch_option.click()
        return self

    def click_duplicate_option(self) -> Self:
        duplicate_option = self.wait10.until(EC.visibility_of_element_located((By.ID, "duplicate-job")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", duplicate_option)
        self.wait10.until(EC.element_to_be_clickable((By.ID, "duplicate-job"))).click()

        return self

    def select_duplicate_item(self, name: str) -> Self:
        option_locator = (By.XPATH,
                          f"//button[contains(@class, 'jenkins-dropdown__item') and contains(text(), '{name}')]")
        self.wait10.until(EC.element_to_be_clickable(option_locator)).click()
        return self

    def is_duplicate_option_displayed(self) -> bool:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "duplicate-job"))).is_displayed()

    def is_from_field_displayed(self) -> bool:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "from"))).is_displayed()

    def select_pipeline(self) -> Self:
        self.driver.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob").click()

        return self

    def get_error_name_message(self) -> str:

        return self.wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'error']"))).text

    def is_error_message_displayed(self) -> bool:

        return self.wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'error']"))).is_displayed()

    def is_ok_button_disabled(self) -> bool:

        return bool(self.wait2.until(EC.element_attribute_to_include((By.ID, "ok-button"), "disabled")))

    def set_duplicate_item_name(self, name) -> Self:
        self.wait2.until(
            EC.visibility_of_element_located((By.ID, "from"))
        ).send_keys(name)

        return self

    def get_duplicate_item_names(self) -> list[str]:
        options = self.wait2.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".jenkins-dropdown__item"))
        )

        return [o.text for o in options]

    def get_no_items_alert_message(self) -> str:
        alert_message = self.wait2.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".jenkins-dropdown__placeholder"))
        ).text
        return alert_message

    def click_ok_expecting_error(self) -> ErrorPage:
        self.wait5.until(EC.element_to_be_clickable(self.OK_BUTTON)).click()
        self.wait5.until_not(EC.url_contains("newJob"))

        return ErrorPage(self.driver)

    def click_ok_expecting_success(self) -> FreestyleConfigurationPage:
        from pages.freestyle_configuration_page import FreestyleConfigurationPage

        self.wait5.until(EC.element_to_be_clickable(self.OK_BUTTON)).click()
        self.wait10.until(EC.visibility_of_element_located((By.NAME, "description")))

        return FreestyleConfigurationPage(self.driver)

    def wait_for_valid_item_name(self) -> Self:
        self.wait10.until(
            EC.text_to_be_present_in_element_attribute(
                (By.ID, "name"),
                "data-valid",
                "true"
            )
        )
        return self

    def is_pipeline_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.PIPELINE_ITEM)).is_displayed()

    def is_items_type_list_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.ITEMS_TYPE_LIST)).is_displayed()

    def get_pipeline_label(self) -> str:
        pipeline_item = self.wait10.until(
            EC.visibility_of_element_located(self.PIPELINE_ITEM)
        )
        return pipeline_item.find_element(
            By.CLASS_NAME,
            "jenkins-choice-list__item__label"
        ).text
