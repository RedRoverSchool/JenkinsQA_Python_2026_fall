import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from common.project_utils import (
    get_browser,
    get_options,
    get_url,
    get_user_name,
    get_password
)


@pytest.fixture
def unauthenticated_browser():
    get_browser()

    try:
        options = webdriver.ChromeOptions()
        for option in get_options():
            options.add_argument(option)

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(6)

        login_url = get_url() + "login?from=%2F"
        driver.get(login_url)

        yield driver

    finally:
        if "driver" in locals():
            driver.quit()


def test_sign_in_valid_credentials(unauthenticated_browser):
    username_field = unauthenticated_browser.find_element(
        By.ID, 'j_username'
    )
    username_field.send_keys(get_user_name())

    password_field = unauthenticated_browser.find_element(
        By.ID, 'j_password'
    )
    password_field.send_keys(get_password())

    sign_in_button = unauthenticated_browser.find_element(
        By.NAME, 'Submit'
    )
    sign_in_button.click()

    current_url = unauthenticated_browser.current_url
    assert current_url == get_url()

    profile_button = unauthenticated_browser.find_element(
        By.XPATH, '//*[@id="root-action-UserAction"]'
    )
    assert profile_button.is_displayed()


