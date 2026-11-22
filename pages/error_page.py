from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ErrorPage(BasePage):
    ERROR_HEADER = (By.CSS_SELECTOR, "#main-panel h1")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "#main-panel p")

    def get_error_header(self) -> str:
        return self.wait5.until(EC.visibility_of_element_located(self.ERROR_HEADER)).text

    def get_error_message(self) -> str:
        return self.wait5.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text