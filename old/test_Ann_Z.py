from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_web_form():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")

    text_box = driver.find_element(By.ID, "username")
    text_box.send_keys("tomsmith")

    password = driver.find_element(By.ID, "password")
    password.send_keys("SuperSecretPassword!")

    button_send = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button_send.click()
    # time.sleep(20)
    message = driver.find_element(By.ID, "flash")
    actual_text = message.text

    driver.quit()
    assert actual_text == "You logged into a secure area!\n×"

