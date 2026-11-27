from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AboutPage(BasePage):
    PAGE_HEADER = (By.CSS_SELECTOR, "#main-panel h1")

    def get_header_text(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.PAGE_HEADER)
        ).text.strip()