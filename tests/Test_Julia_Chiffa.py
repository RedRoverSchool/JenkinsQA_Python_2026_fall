from selenium import webdriver
from selenium.webdriver.common.by import By

def test_second()-> None:
    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    title = driver.title

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="user-name")
    submit_button = driver.find_element(by=By.NAME, value="login-button")

    text_box.send_keys("standard_user")
    submit_button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value='.error-message-container.error')
    assert message.text == "Epic sadface: Password is required"

    driver.quit()
