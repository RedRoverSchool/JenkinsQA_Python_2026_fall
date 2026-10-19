from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_valid_login_and_password():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    login_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    my_login = "standard_user"
    my_password = "secret_sauce"

    login_input.send_keys(my_login)
    password_input.send_keys(my_password)
    login_button.click()

    time.sleep(1)

    current_url = driver.current_url

    # проверка перехода в личный кабинет после успешной авторизации
    assert current_url == "https://www.saucedemo.com/inventory.html", "incorrect URL"

    driver.quit()

def test_valid_login_and_invalid_password():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    login_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    my_login = "standard_user"
    my_password = "123"

    login_input.send_keys(my_login)
    password_input.send_keys(my_password)
    login_button.click()

    time.sleep(1)

    current_url = driver.current_url
    error_message = driver.find_element(By.CSS_SELECTOR, "h3")

    # проверка, что не осуществляется переход на другой урл и баннера с ошибкой
    assert current_url == "https://www.saucedemo.com/", "incorrect URL"
    assert error_message.text == "Epic sadface: Username and password do not match any user in this service", "incorrect message"

    driver.quit()
