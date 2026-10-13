from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def test_text_input():
    driver = webdriver.Chrome()
    driver.get("https://qapracticehub.com/?utm_source=chatgpt.com#inputs")


    text_box = driver.find_element(By.ID, "text-input")
    text_box.click()
    text_box.send_keys("Ekaterina")
    assert text_box.get_attribute("value") == "Ekaterina"
    label = driver.find_element(By.CSS_SELECTOR, '[for="text-input"]')
    assert label.text == "Text Input"
    time.sleep(5)
    driver.quit()

def test_login():
    driver = webdriver.Chrome()
    driver.get("https://qapracticehub.com/?utm_source=chatgpt.com#forms")
    wait = WebDriverWait(driver, 10)

    username_field = wait.until(
        EC.element_to_be_clickable((By.ID, "login-username"))
    )
    username_field.click()
    time.sleep(5)
    username_field.send_keys("tester")

    password_field = wait.until(
        EC.element_to_be_clickable((By.ID, "login-password"))
    )
    username_field.click()
    time.sleep(5)
    password_field.send_keys("password123")

    submit_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login-submit"))
    )
    time.sleep(5)
    submit_button.click()

    message_element = wait.until(
        EC.visibility_of_element_located((By.ID, "login-message"))
    )

    message_text = message_element.text
    expected = "Login successful! Welcome, tester."
    assert expected in message_text, f"Ожидалось: {expected}, получили: {message_text}"

    time.sleep(20)
    driver.quit()