import time
from selenium.webdriver.common.by import By

def test_welcome_to_jenkins(browser):
    welcome_title = browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")

    assert welcome_title.text == "Welcome to Jenkins!"
