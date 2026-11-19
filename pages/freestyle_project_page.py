from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.freestyle_configuration_page import FreestyleConfigurationPage


class FreestyleProjectPage(BasePage):

    def click_configuration(self):
        self.driver.find_element(By.XPATH, "//a[contains(., 'Configure')]").click()

        return FreestyleConfigurationPage(self.driver)
