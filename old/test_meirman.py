import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

browser = webdriver.Chrome(options=options)
BASE_URL = "https://www.saucedemo.com/"

username_field = (By.ID, "user-name")
password_field = (By.ID, "password")
login_button = (By.ID, "login-button")


def test_example():
    browser.get(BASE_URL)
    browser.find_element(*username_field).send_keys("standard_user")
    browser.find_element(*password_field).send_keys("secret_sauce")
    browser.find_element(*login_button).click()
    logo_text = browser.find_element(By.XPATH, '//div[@class="app_logo"]').text
    assert logo_text == 'Swag Labs'
    browser.close()
