from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.project_utils import get_user_name, get_password, get_url
from common.jenkins_utils import logout

def test_successful_login(browser):

    username = get_user_name()
    password = get_password()
    base_url = get_url()
    logout(browser)

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "j_username"))
    )

    browser.find_element(By.ID, "j_username").send_keys(username)
    browser.find_element(By.NAME, "j_password").send_keys(password)
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']"))
    )
    assert "login" not in browser.current_url


def test_login_with_invalid_credentials(browser):

    username = get_user_name()
    logout(browser)

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "j_username"))
    )
    browser.find_element(By.ID, "j_username").send_keys(username)
    browser.find_element(By.NAME, "j_password").send_keys("WrongPassword_12345!")
    browser.find_element(By.NAME, "Submit").click()

    error_message = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid username or password')]"))
    )

    assert "Invalid username or password" in error_message.text