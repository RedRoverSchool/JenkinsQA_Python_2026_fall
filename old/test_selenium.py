from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_first():
    driver = webdriver.Chrome()

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    assert message.text == "Received!"

    driver.quit()

def test_login():
    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")

    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # assert "inventory" in driver.current_url

    products_title = driver.find_element(By.CLASS_NAME, "title")

    assert products_title.text == "Products"

    driver.quit()

    time.sleep(10)

def test_second():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://tradematix.com")

    time.sleep(5)

    assert driver.title == "Tradematix - Next-gen Trading Tools"
    element = driver.find_element(By.CSS_SELECTOR, ".tn-atom__button-text")
    element.click()

    assert driver.current_url == "https://tradematix.com/#rec802399224"
    driver.quit()

def test_third():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    driver.get("https://www.trip.com/")
    time.sleep(2)

    language_icon = driver.find_element(by=By.CLASS_NAME, value="locale-icon")
    time.sleep(4)
    current_language = language_icon.get_attribute("class")

    if "flag-en" not in current_language:
        language_icon.click()
        language_change = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//span[contains(@class, "mc-lhd-locale-item-country") '
                'and normalize-space()="English"]'
            ))
        )
        language_change.click()
    time.sleep(4)

    assert "Trip.com Official Site" in driver.title

    flights = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#header_action_nav_flights > div.mc-lhd-sider-nav-item-content"
        ))
    )
    flights.click()
    title = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#trip_main_content > div.top-wrapper > div.inner-wrapper > div.inner-title > h1"
        ))
    )

    assert title.text == "Discover the best flight deals"
    driver.quit()