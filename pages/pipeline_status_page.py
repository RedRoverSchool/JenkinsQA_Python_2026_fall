from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.pipeline_configuration_page import PipelineConfigurationPage

class PipelineStatusPage(BasePage):

    def get_configuration_description(self) -> str:
        return self.wait10.until(EC.visibility_of_element_located((By.ID, "view-message"))).text

    def open_configuration_pipeline_page(self) -> PipelineConfigurationPage:
        self.driver.find_element(By.CSS_SELECTOR, "a[href$=configure]").click()

        return PipelineConfigurationPage(self.driver)
