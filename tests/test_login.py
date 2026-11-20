from common.project_utils import get_user_name, get_password
from common.jenkins_utils import logout
from pages.login_page import LoginPage


def test_successful_login(browser, wait10):
    username = get_user_name()
    password = get_password()
    logout(browser)

    LoginPage(browser).login(username, password)

    assert "login" not in browser.current_url


def test_login_with_invalid_credentials(browser, wait10):
    username = get_user_name()
    logout(browser)

    login_page = LoginPage(browser)
    login_page.login(username, "WrongPassword_12345!")

    error_text = login_page.get_error_message()
    assert "Invalid username or password" in error_text