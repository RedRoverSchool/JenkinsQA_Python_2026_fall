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