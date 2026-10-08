from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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