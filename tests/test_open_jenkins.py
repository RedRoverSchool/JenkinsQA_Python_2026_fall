import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from old.test_meirman import browser


def test_open_jenkins(browser):
    time.sleep(5)
    label = browser.find_element(By.XPATH,"//h1[text()='Welcome to Jenkins!']")
    assert label.text == "Welcome to Jenkins!"


def test_new_item_page_open(browser):
    time.sleep(2)
    new_item  = browser.find_element(By.CSS_SELECTOR,"a[href='/view/all/newJob']")
    new_item.click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'

