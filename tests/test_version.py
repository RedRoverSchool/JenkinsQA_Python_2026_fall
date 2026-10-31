import time
from selenium.webdriver.common.by import By


def test_jenkins_version(browser):
    rest_api_button = browser.find_element(
        By.XPATH, "/html/body/footer/div/div[2]/a")

    rest_api_button.click()

    jenkins_version_button = browser.find_element(
        By.XPATH, "/html/body/footer/div/div[2]/button")
    browser.execute_script(
        "arguments[0].scrollIntoView(true);", jenkins_version_button)

    assert jenkins_version_button.text == "Jenkins 2.580.1"

