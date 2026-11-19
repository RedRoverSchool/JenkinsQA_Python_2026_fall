from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.new_item_page import NewItemPage


class HomePage(BasePage):

    def click_new_item(self):
        self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/view/all/newJob']"))).click()

        return NewItemPage(self.driver)

    def get_first_project_name(self):
        return self.wait5.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".jenkins-table__link >span:first-child"))).text
