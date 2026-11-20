from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.home_page import HomePage


class LoginPage(BasePage):

    def login(self, username: str, password: str) -> HomePage:
        self.wait10.until(EC.visibility_of_element_located((By.ID, "j_username"))).send_keys(username)
        self.driver.find_element(By.NAME, "j_password").send_keys(password)
        self.driver.find_element(By.NAME, "Submit").click()
        return HomePage(self.driver)

    def get_error_message(self) -> str:
        error = self.wait10.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid username or password')]")))

        return error.text
