import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By



def test_open_base_page():
    driver = webdriver.Chrome()
    driver.get("https://automationteststore.com/")
    assert driver.current_url == "https://automationteststore.com/"
    driver.quit()

def test_open_login_page():
    driver = webdriver.Chrome()
    driver.get("https://automationteststore.com/")
    driver.implicitly_wait(5)
    LOGIN_OR_REGISTER = driver.find_element(By.XPATH,"//a[text()='Login or register']")
    LOGIN_OR_REGISTER.click()
    titel = driver.title
    print(titel)
    assert titel == "Account Login"
    driver.quit()


def test_create_account_page():
    driver = webdriver.Chrome()
    driver.get("https://automationteststore.com/")
    driver.implicitly_wait(5)
    LOGIN_OR_REGISTER = driver.find_element(By.XPATH, "//a[text()='Login or register']")
    LOGIN_OR_REGISTER.click()
    BTN_CONTINEUM = driver.find_element(By.XPATH, "//button[@title='Continue']")
    BTN_CONTINEUM.click()
    title = driver.title
    assert title == "Create Account"
    driver.quit()


def test_open_shoping_cart():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://automationteststore.com/")
    driver.implicitly_wait(5)
    CARD_LINK1 = driver.find_element(By.XPATH, "(//li[@data-id='menu_cart'])[1]").click()
    title = driver.title
    assert title == "Shopping Cart"
    driver.quit()

def test_create_new_account():
    driver = webdriver.Chrome()
    driver.get("https://automationteststore.com/index.php?rt=account/create")
    driver.implicitly_wait(5)
    FIRST_NAME_FILD = driver.find_element(By.XPATH, "//input[@id='AccountFrm_firstname']").send_keys('Ruslan')
    LAST_NAME_FILD = driver.find_element(By.XPATH,"//input[@id='AccountFrm_lastname']").send_keys('Khasanov')
    EMAIL_FILD = driver.find_element(By.XPATH, "//input[@id='AccountFrm_email']").send_keys(f'5553email@gmail.com')
    PHONE_NUMBER = driver.find_element(By.XPATH,"//input[@id='AccountFrm_telephone']").send_keys('9601458869')
    ADDRES_FILD_1 = driver.find_element(By.XPATH,"//input[@id='AccountFrm_address_1']").send_keys('Baiker street 43')
    COUNTRY_CHOSE = driver.find_element(By.XPATH,"//option[@value='223']").click()
    REGION_CHOUSE = driver.find_element(By.XPATH,"//option[@value='3669']").click()
    CHOUSE_CITY = driver.find_element(By.XPATH,"//input[@id='AccountFrm_city']").send_keys('AUSTIN')
    LOGIN_FILD = driver.find_element(By.XPATH,"//input[@id='AccountFrm_loginname']").send_keys('Ru44444an')
    PASSWORD_FILD = driver.find_element(By.XPATH,"//input[@id='AccountFrm_password']").send_keys('Parole123')
    CONFIRM_PASSWORD = driver.find_element(By.XPATH,"//input[@id='AccountFrm_confirm']").send_keys('Parole123')
    ZIP_CODE = driver.find_element(By.XPATH,"//input[@id='AccountFrm_postcode']").send_keys('77356')
    AGREE_ACAUNT = driver.find_element(By.XPATH,"//input[@id='AccountFrm_agree']").click()
    BTN_CONTINUE = driver.find_element(By.XPATH,"//button[@title='Continue']").click()
    time.sleep(10)
    title = driver.title
    print(title)
    assert title == "Your Account Has Been Created!"
    time.sleep(10)
    driver.quit()


