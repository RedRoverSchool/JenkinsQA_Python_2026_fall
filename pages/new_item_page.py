from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.folder_configuration_page import FolderConfigurationPage
from pages.freestyle_configuration_page import FreestyleConfigurationPage
from pages.pipeline_configuration_page import PipelineConfigurationPage


class NewItemPage(BasePage):
    def set_item_name(self, name: str) -> Self:
        self.wait10.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys(name)

        return self

    def select_freestyle_and_click_ok(self) -> FreestyleConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "hudson_model_FreeStyleProject").click()
        self.driver.find_element(By.ID, "ok-button").click()

        return FreestyleConfigurationPage(self.driver)

    def select_folder_and_click_ok(self) -> FolderConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "com_cloudbees_hudson_plugins_folder_Folder").click()
        self.driver.find_element(By.ID, "ok-button").click()

        # wait new page
        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return FolderConfigurationPage(self.driver)

    def select_pipeline_and_click_ok(self) -> PipelineConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob").click()

        # wait ok button
        self.wait2.until(EC.element_to_be_clickable((By.ID, "ok-button"))).click()

        # wait new page
        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return PipelineConfigurationPage(self.driver)
