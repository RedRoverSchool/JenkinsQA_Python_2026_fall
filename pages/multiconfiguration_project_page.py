from selenium.webdriver.common.by import By

from pages import multiconfiguration_configuration_page
from pages.base_page import BasePage
from pages.multiconfiguration_configuration_page import MulticonfigurationConfigurationPage

class MulticonfigurationProjectPage(BasePage):

    def get_description(self) -> MulticonfigurationConfigurationPage:
        return self.driver.find_element(By.ID, "description-content").text

    def get_configure(self) -> MulticonfigurationConfigurationPage:
        self.driver.find_element(By.XPATH, "//a[contains(@href,'/configure')]").click()

        return MulticonfigurationConfigurationPage(self.driver)