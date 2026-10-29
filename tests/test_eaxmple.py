import time
from selenium.webdriver.common.by import By

def test_welcome_to_jenkins(browser):
    assert "Welcome to Jenkins!" == browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")
