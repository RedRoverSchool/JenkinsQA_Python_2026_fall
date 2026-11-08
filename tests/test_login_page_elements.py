import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from common.project_utils import get_browser, get_options, get_url


@pytest.fixture(scope="function")
def unauthenticated_browser(request):
    get_browser()

    try:
        options = webdriver.ChromeOptions()
        for option in get_options():
            options.add_argument(option)

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

        login_url = get_url() + "login?from=%2F"
        driver.get(login_url)

        yield driver

    finally:
        if "driver" in locals():
            driver.quit()


def test_login_page_elements(unauthenticated_browser):
    heading = unauthenticated_browser.find_element(
        By.XPATH, '//*[@id="main-panel"]/div/h1'
    )
    assert heading.is_displayed()
    assert heading.text == 'Sign in to Jenkins'

    username_label = unauthenticated_browser.find_element(
        By.XPATH, '//*[@id="main-panel"]/div/form/div[1]/label'
    )
    assert username_label.is_displayed()
    assert username_label.text == 'Username'

    username_field = unauthenticated_browser.find_element(
        By.ID, 'j_username'
    )
    assert username_field.is_displayed()
    assert username_field.is_enabled()

    password_label = unauthenticated_browser.find_element(
        By.XPATH, '//*[@id="main-panel"]/div/form/div[2]/label'
    )
    assert password_label.is_displayed()
    assert password_label.text == 'Пароль'

    password_field = unauthenticated_browser.find_element(
        By.ID, 'j_password'
    )
    assert password_field.is_displayed()
    assert password_field.is_enabled()

    checkbox_label = unauthenticated_browser.find_element(
        By.XPATH, '//*[@id="main-panel"]/div/form/div[3]/label'
    )
    assert checkbox_label.is_displayed()
    assert checkbox_label.text == 'Keep me signed in'

    checkbox = unauthenticated_browser.find_element(
        By.ID, 'remember_me'
    )
    assert checkbox.is_displayed()
    assert checkbox.is_enabled()
    assert not checkbox.is_selected()

    sign_in_button = unauthenticated_browser.find_element(
        By.NAME, 'Submit'
    )
    assert sign_in_button.is_displayed()
    assert sign_in_button.text == 'Sign in'
    assert sign_in_button.is_enabled()