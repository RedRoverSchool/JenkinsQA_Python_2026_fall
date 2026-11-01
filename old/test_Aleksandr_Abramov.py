from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_saucedemo():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    assert driver.title == "Swag Labs"
    time.sleep(2)

    login = driver.find_element(By.ID, "user-name")
    login.send_keys("standard_user")

    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")

    submit_button = driver.find_element(By.XPATH, '//*[@id="login-button"]')
    submit_button.click()
    time.sleep(2)

    driver.quit()