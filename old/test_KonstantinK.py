from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Base_URL = "https://www.saucedemo.com/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
EXPECTED_PAGE_TITLE = "Products"


class Authorisation:
    USER_NAME_FIELD = (By.CSS_SELECTOR, '#user-name')
    PASSWORD_FIELD = (By.CSS_SELECTOR, '#password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '#login-button')
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")

def test_authorisation(driver):
    driver.get(Base_URL)
    driver.find_element(*Authorisation.USER_NAME_FIELD).send_keys(USERNAME)
    driver.find_element(*Authorisation.PASSWORD_FIELD).send_keys(PASSWORD)
    driver.find_element(*Authorisation.LOGIN_BUTTON).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(Authorisation.PRODUCTS_TITLE))
    page_title = driver.find_element(*Authorisation.PRODUCTS_TITLE).text
    current_url = driver.current_url
    assert current_url == INVENTORY_URL, f" Actual url {current_url} Expected url  {INVENTORY_URL}"
    assert  EXPECTED_PAGE_TITLE == page_title, f" Actual title {page_title} Expected title  {EXPECTED_PAGE_TITLE}"
