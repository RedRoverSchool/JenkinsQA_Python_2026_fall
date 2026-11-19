from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class FolderPage(BasePage):

    def get_configuration_description(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "view-message"))).text
