from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://www.saucedemo.com/"
username = "standard_user"
password = "secret_sauce"

def test_autorization():
    driver = webdriver.Chrome()
    driver.get(base_url)

    login_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "user-name")))
    login_field.send_keys(username)

    passw_field = driver.find_element(By.ID, "password")
    passw_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    items_list = WebDriverWait(driver, 5).until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "[class = 'inventory_item_name ']")))
    assert len(items_list) > 0, "Авторизация не пройдена "

    driver.quit()