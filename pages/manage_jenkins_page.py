from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ManageJenkinsPage(BasePage):
    def get_group_names(self):
        return [el.text for el in
                self.driver.find_elements(By.XPATH, "//section[contains(@class,'jenkins-section')]/h2")]

    def get_option_names(self):
        return [el.text for el in
                self.driver.find_elements(By.XPATH, "//section[contains(@class,'jenkins-section')]//dt")]

    def get_page_title(self) -> str:
        heading = self.wait10.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        return heading.text
