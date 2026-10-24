from selenium import webdriver
from selenium.webdriver.common.by import By

def test_web_form1():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    text_box_username = driver.find_element(By.ID,"user-name")
    text_box_password = driver.find_element(By.ID,"password")

    text_box_username.send_keys("standard_user")
    text_box_password.send_keys("secret_sauce")

    button = driver.find_element(By.ID, "login-button")
    button.click()

    assert driver.current_url=="https://www.saucedemo.com/inventory.html"
    driver.quit()