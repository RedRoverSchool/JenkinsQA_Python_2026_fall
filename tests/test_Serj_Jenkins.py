from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_jenkins_1():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8080")
    time.sleep(2)

    username_field = driver.find_element(by=By.NAME, value='j_username')
    assert username_field.is_displayed()
    username_field.click()
    username_field.send_keys('admin')
    password_field = driver.find_element(by=By.NAME, value='j_password')
    assert password_field.is_displayed()
    password_field.click()
    password_field.send_keys('admin')
    signin_field = driver.find_element(by=By.NAME, value='Submit')
    assert signin_field.is_displayed()
    signin_field.click()
    header = driver.find_element(by=By.XPATH, value='//*[@id="main-panel"]/div[2]/div/h1')
    assert header.is_displayed()
    assert header.text == 'Welcome to Jenkins!'