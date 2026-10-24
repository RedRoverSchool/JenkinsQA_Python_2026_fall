from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_login_to_site():
    driver = webdriver.Chrome()
    driver.get("https://shawarma.threadqa.ru/login")
    login = driver.find_element(By.XPATH, "//input[@data-testid='login-username']")
    login.click()
    login.send_keys("owner")
    password = driver.find_element(By.XPATH, "//input[@data-testid='login-password']")
    password.send_keys("owner123")
    submit_button = driver.find_element(By.XPATH, "//button[@data-testid='login-submit']")
    submit_button.click()
    assert driver.current_url == "https://shawarma.threadqa.ru/login"
    time.sleep(9)
    driver.quit()