from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.project_utils import get_user_name, get_password
from common.jenkins_utils import logout
from pages.login_page import LoginPage


def test_successful_login(browser, wait10):
    username = get_user_name()
    password = get_password()
    logout(browser)

    LoginPage(browser).login(username, password)

    wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))


def test_login_with_invalid_credentials(browser, wait10):
    username = get_user_name()
    logout(browser)

    login_page = LoginPage(browser)

    login_page.driver.find_element(By.ID, "j_username").send_keys(username)
    login_page.driver.find_element(By.NAME, "j_password").send_keys("WrongPassword_12345!")
    login_page.driver.find_element(By.NAME, "Submit").click()

    error_text = login_page.get_error_message()

    assert "Invalid username or password" in error_text