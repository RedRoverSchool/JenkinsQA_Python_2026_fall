from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

from selenium.webdriver.support import expected_conditions as EC

class FolderConfigurationPage(BasePage):
    def set_display_name(self, display_name: str) -> Self:
        self.driver.find_element(By.NAME, "_.displayNameOrNull").send_keys(display_name)

        return self

    def click_apply(self) -> Self:
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()

        return self

    def click_submit(self) -> 'FolderPage':
        from pages.folder_page import FolderPage
        self.wait10.until(EC.visibility_of_element_located((By.NAME, "Submit"))).click()
        return FolderPage(self.driver)

    def set_dicription(self, dicription: str) -> Self:
        self.driver.find_element(By.NAME,"_.description").send_keys(dicription)

        return self

    def get_display_name(self) -> str:
        return self.driver.find_element(By.NAME, "_.displayNameOrNull").get_attribute("value")

    def get_description(self) -> str:
        return self.driver.find_element(By.NAME, "_.description").get_attribute("value")