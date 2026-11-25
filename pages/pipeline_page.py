from typing import Self

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.pipeline_configuration_page import PipelineConfigurationPage

class PipelinePage(BasePage):
    EDIT_DESCRIPTION_BTN = (By.XPATH, "//*[@id='description-link']/span")
    DESCRIPTION_CONTENT_FLD = (By.XPATH, "//*[@id='description-content']")

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

    def open_configuration_pipeline_page(self) -> PipelineConfigurationPage:
        self.driver.find_element(By.CSS_SELECTOR, "a[href$=configure]").click()

        return PipelineConfigurationPage(self.driver)

    def click_add_or_rename_description_btn(self):
        edit_desc_btm = self.wait10.until(EC.element_to_be_clickable(self.EDIT_DESCRIPTION_BTN))
        edit_desc_btm.click()
        return self

    def is_description_empty(self) -> bool:
        try:
            self.wait10.until(
                lambda driver: len(driver.find_elements(*self.DESCRIPTION_CONTENT_FLD)) == 0
                               or driver.find_element(*self.DESCRIPTION_CONTENT_FLD).text.strip() == ""
            )
            return True
        except TimeoutException:
            return False
