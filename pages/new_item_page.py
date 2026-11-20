from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.folder_configuration_page import FolderConfigurationPage
from pages.freestyle_configuration_page import FreestyleConfigurationPage


class NewItemPage(BasePage):
    def set_item_name(self, name: str) -> Self:
        self.wait10.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys(name)

        return self

    def select_freestyle_and_click_ok(self) -> FreestyleConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "hudson_model_FreeStyleProject").click()
        self.driver.find_element(By.ID, "ok-button").click()

        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return FreestyleConfigurationPage(self.driver)

    def select_folder_and_click_ok(self) -> FolderConfigurationPage:
        self.driver.find_element(By.CLASS_NAME, "com_cloudbees_hudson_plugins_folder_Folder").click()
        self.driver.find_element(By.ID, "ok-button").click()

        self.wait10.until(EC.presence_of_element_located((By.ID, "side-panel")))

        return FolderConfigurationPage(self.driver)

    def click_duplicate_option(self) -> Self:
        duplicate_option = self.wait10.until(EC.visibility_of_element_located((By.ID, "duplicate-job")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", duplicate_option)
        self.wait10.until(EC.element_to_be_clickable((By.ID, "duplicate-job"))).click()

        return self

    def is_duplicate_option_displayed(self) -> bool:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "duplicate-job"))).is_displayed()

    def is_from_field_displayed(self) -> bool:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "from"))).is_displayed()