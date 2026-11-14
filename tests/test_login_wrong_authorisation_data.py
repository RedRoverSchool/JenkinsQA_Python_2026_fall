from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.project_utils import get_user_name, get_password, get_url
from common.jenkins_utils import logout


def test_jenkins_login(browser):
    browser.get(get_url())

    assert browser.title == "Sign in - Jenkins"
    browser.find_element(By.ID, "j_username").send_keys("test")
    browser.find_element(By.ID, "j_password").send_keys("test")
    browser.find_element(By.NAME, "Submit").click()
    #time.sleep(3)

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "app-sign-in-register__error")))
    warning_text = browser.find_element(By.CLASS_NAME, "app-sign-in-register__error").text
    assert warning_text == "Invalid username or password"
    #time.sleep(10)