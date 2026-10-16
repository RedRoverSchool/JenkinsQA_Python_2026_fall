from selenium import webdriver
from selenium.webdriver.common.by import By


def test_authorization():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(0.5)
    text_box_login=driver.find_element(by=By.NAME, value="user-name")##поле логин
    text_box_password=driver.find_element(by=By.NAME, value="password")##поле пароль
    text_box_login.send_keys("standard_user")##ввод логина
    text_box_password.send_keys("secret_sauce")##ввод пароля
    login_button=driver.find_element(by=By.NAME, value="login-button")##кнопка
    login_button.click()
    header = driver.find_element(By.CLASS_NAME, "app_logo")
    assert header.text == "Swag Labs"
    driver.close()