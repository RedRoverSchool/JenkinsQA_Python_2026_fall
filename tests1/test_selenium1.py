from selenium import webdriver
from selenium.webdriver.common.by import By


def test_first():
    driver = webdriver.Chrome()

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    text = message.text

    assert message.text == "Received!"


    driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_login():
    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")

    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # assert "inventory" in driver.current_url

    products_title = driver.find_element(By.CLASS_NAME, "title")

    assert products_title.text == "Products"


    driver.quit()

    time.sleep(10)