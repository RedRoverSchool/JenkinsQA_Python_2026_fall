from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class MultibranchConfigurationPage(BasePage):

    def click_apply(self) -> Self:
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()

        return self
