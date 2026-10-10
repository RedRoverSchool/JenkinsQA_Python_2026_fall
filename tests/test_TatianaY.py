from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

USER_NAME = (By.XPATH, "//*[@id='user-name']")
PASSWORD = (By.XPATH, "//*[@id='password']")
LOGIN = (By.XPATH, "//*[@id='login-button']")
ADD_TO_CARD_BTN = (By.XPATH, "//*[@id='add-to-cart-sauce-labs-backpack']")
CARD = (By.XPATH, "//*[@id='shopping_cart_container']/a")
ITEM = (By.XPATH, "//*[@id='item_4_title_link']/div")
ITEM_IN_CARD = (By.XPATH, "//*[@id='item_4_title_link']/div")
BURGER_MENU = (By.XPATH, "//button[@id='react-burger-menu-btn']")
LOGOUT = (By.XPATH, "//*[@id='logout_sidebar_link']")

def test_add_item_to_card():
    chrome_options = Options()
    # Отключаем встроенную проверку утечки паролей
    chrome_options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.saucedemo.com/')
    driver.find_element(*USER_NAME).send_keys("standard_user")
    driver.find_element(*PASSWORD).send_keys("secret_sauce")
    driver.find_element(*LOGIN).click()
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", 'url не соответствует ожидаемому'
    text_before = driver.find_element(*ITEM).text
    driver.find_element(*ADD_TO_CARD_BTN).click()
    driver.find_element(*CARD).click()
    text_after = driver.find_element(*ITEM_IN_CARD).text
    assert text_before == text_after
    driver.quit()

def test_auth_positive():
    chrome_options = Options()
    # Отключаем встроенную проверку утечки паролей
    chrome_options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.saucedemo.com/')
    driver.find_element(*USER_NAME).send_keys("standard_user")
    driver.find_element(*PASSWORD).send_keys("secret_sauce")
    driver.find_element(*LOGIN).click()
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", 'url не соответствует ожидаемому'
    time.sleep(1)
    driver.quit()



def test_logout():
    chrome_options = Options()
    # Отключаем встроенную проверку утечки паролей
    chrome_options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.saucedemo.com/')
    driver.find_element(*USER_NAME).send_keys("standard_user")
    driver.find_element(*PASSWORD).send_keys("secret_sauce")
    driver.find_element(*LOGIN).click()
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", 'url не соответствует ожидаемому'
    driver.find_element(*BURGER_MENU).click()
    time.sleep(1)
    driver.find_element(*LOGOUT).click()
    assert driver.current_url == "https://www.saucedemo.com/"
    driver.quit()

