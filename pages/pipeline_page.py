from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class PipelinePage(BasePage):

    def get_configuration_description(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "view-message"))).text

    def get_warning_message(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "enable-project"))).text.split('\n')[0].strip()

    def is_enabled_button_visible(self) -> bool:
        return bool(self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[value='Enable']"))).is_displayed())

    def click_rename(self) -> Self:
        self.wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$='/confirm-rename']"))).click()

        return self

    def rename_and_submit(self, new_name) -> Self:
        name_field = self.wait5.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[name='newName']")))
        name_field.clear()
        name_field.send_keys(new_name)

        self.driver.find_element(By.CSS_SELECTOR, "[name='Submit']").click()

        return self

    def get_actual_name(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".job-index-headline"))).text
