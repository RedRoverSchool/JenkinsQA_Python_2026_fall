from selenium import webdriver
from selenium.webdriver.common.by import By
import random

BASE_URL = 'https://www.saucedemo.com/'
target_url = "https://www.saucedemo.com/inventory.html"

correct_username = ['standard_user', 'locked_out_user', 'problem_user', 'performance_glitch_user', 'error_user', 'visual_user']
correct_password = 'secret_sauce'

incorrect_username = 'test'
incorrect_password = '12345qwerty'

def login_elements(driver):
    login_input = driver.find_element(By.CSS_SELECTOR, "[data-test='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "[data-test='password']")
    login_button = driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']")

    return login_input, password_input, login_button

def login_error_elements(driver):
    error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    error_button = driver.find_element(By.CSS_SELECTOR, "[data-test='error-button']")

    return error_message, error_button

def test_authorisation():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    login_input, password_input, login_button = login_elements(driver)

    login_input.send_keys(random.choice(correct_username))
    password_input.send_keys(correct_password)
    login_button.click()

    assert driver.current_url == target_url

    driver.quit()

def test_empty_login_fields():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    login_input, password_input, login_button = login_elements(driver)

    login_button.click()

    error_message, error_button = login_error_elements(driver)

    assert error_message.text == 'Epic sadface: Username is required'
    assert error_button.is_displayed()

    driver.quit()

def test_incorrect_login():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    login_input, password_input, login_button = login_elements(driver)

    login_input.send_keys(incorrect_username)
    password_input.send_keys(correct_password)
    login_button.click()

    error_message, error_button = login_error_elements(driver)

    assert error_message.text == 'Epic sadface: Username and password do not match any user in this service'
    assert error_button.is_displayed()

    driver.quit()


def test_incorrect_password():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    login_input, password_input, login_button = login_elements(driver)

    login_input.send_keys(random.choice(correct_username))
    password_input.send_keys(incorrect_password)
    login_button.click()

    error_message, error_button = login_error_elements(driver)

    assert error_message.text == 'Epic sadface: Username and password do not match any user in this service'
    assert error_button.is_displayed()

    driver.quit()