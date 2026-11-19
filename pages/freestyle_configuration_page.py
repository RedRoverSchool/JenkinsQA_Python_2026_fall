from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FreestyleConfigurationPage(BasePage):

    def click_project_save(self):
        self.driver.find_element(By.NAME, "Submit").click()
        from pages.freestyle_project_page import FreestyleProjectPage

        return FreestyleProjectPage(self.driver)
