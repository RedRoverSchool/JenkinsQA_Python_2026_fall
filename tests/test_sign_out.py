from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def test_redirect_to_login_page_after_logout(browser):

    protected_url = browser.current_url

    user_menu_btn = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "root-action-UserAction"))
    )
    ActionChains(browser).move_to_element(user_menu_btn).perform()

    WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="/logout"]'))
    ).click()

    assert len(browser.find_elements(By.CSS_SELECTOR,
                                     ".jenkins-dialog, .modal, .alert, .warning, .error")) == 0, \
        'Any notification received or confirmation required'

    assert WebDriverWait(browser, timeout=10).until(EC.url_contains("login")), "No redirect to login page after logout"

    login_field_value = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "j_username"))).get_attribute("value")
    password_field_value = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "j_password"))).get_attribute("value")

    assert login_field_value == "", "Login field is not empty"
    assert password_field_value == "", "Password field is not empty"

    browser.get(protected_url)

    assert WebDriverWait(browser, 10).until(EC.url_contains("login")), \
        "User still has access to protected page after logout"
