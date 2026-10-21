from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    burger_menu = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
    burger_menu.click()
    logout_button = wait.until(EC.visibility_of_element_located((By.ID, "logout_sidebar_link")))

    assert logout_button.text == "Logout"


def test_confirm_product(driver):

    wait = WebDriverWait(driver, 10)
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    product = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), "
                                                                     "'Sauce Labs Fleece Jacket')]")))
    product.click()

    back_button = wait.until(EC.visibility_of_element_located((By.ID, "back-to-products")))
    assert back_button.is_displayed()

    title = driver.find_element(By.CLASS_NAME, "inventory_details_name")
    assert title.text == 'Sauce Labs Fleece Jacket'
