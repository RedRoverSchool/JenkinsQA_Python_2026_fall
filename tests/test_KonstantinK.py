from selenium.webdriver.common.by import By


BaseURL = "https://www.saucedemo.com/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

class Authorisation:
    USER_NAME_FIELD  = (By.CSS_SELECTOR, '#user-name')
    PASSWORD_FIELD = (By.CSS_SELECTOR, '#password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '#login-button')



def test_authorisation(driver):
    driver.get(BaseURL)
    driver.find_element(*Authorisation.USER_NAME_FIELD).send_keys(USERNAME)
    driver.find_element(*Authorisation.PASSWORD_FIELD).send_keys(PASSWORD)
    driver.find_element(*Authorisation.LOGIN_BUTTON).click()
    current_url = driver.current_url
    assert current_url == INVENTORY_URL,  f" Actual url {current_url}  not equals Expected url  {INVENTORY_URL}"



