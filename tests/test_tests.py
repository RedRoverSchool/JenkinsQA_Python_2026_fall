import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def wait(browser):
    wait = WebDriverWait(browser, timeout=10)
    return wait


VERSION_BTN = (By.XPATH, "//*[@id='jenkins']/footer/div/div[2]/button")
WEBSITE_BTN = (By.XPATH, "//*[@id='tippy-2']/div/div/div/a[3]")
TEXT = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[3]/h1/span")


def test_version(browser, wait):

    wait.until(EC.element_to_be_clickable(VERSION_BTN)).click()
    wait.until(EC.element_to_be_clickable(WEBSITE_BTN)).click()
    wait.until(EC.url_contains("jenkins.io"))
    label = wait.until(EC.presence_of_element_located(TEXT))
    assert "Jenkins" in label.text


