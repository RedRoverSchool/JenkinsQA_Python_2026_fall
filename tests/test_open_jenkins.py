import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_open_jenkins(browser):
    time.sleep(5)
    label = browser.find_element(By.XPATH, "//h1[text()='Welcome to Jenkins!']")
    assert label.text == "Welcome to Jenkins!"


def test_new_item_page_open(browser):
    time.sleep(2)
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'

def test_create_new_folder(browser):
    time.sleep(2)
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'
    name_new_item = browser.find_element(By.XPATH, "//input[@id='name']").send_keys("folder_name")
    assert browser.find_element(By.XPATH, "//input[@id='name']").get_attribute('value') == "folder_name"
    folder_link = browser.find_element(By.XPATH,"//span[text()='Folder']").click()
    btn_ok = browser.find_element(By.XPATH, "//button[@id='ok-button']").click()
    time.sleep(2)
    assert browser.find_element(By.XPATH, "(//div[@class='jenkins-app-bar__content'])[1]").is_displayed()
    display_name_fild = browser.find_element(By.XPATH, "//input[@name='_.displayNameOrNull']").send_keys("Display")
    discrip_filde = browser.find_element(By.XPATH,"//textarea[@name='_.description']").send_keys("Description hello world")
    btn_save = browser.find_element(By.XPATH, "//button[@value='Save']").click()
    time.sleep(2)
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()


def test_open_builds_history(browser):
    time.sleep(2)
    builds_history_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/builds']")
    builds_history_link.click()
    assert browser.current_url == "http://localhost:8080/view/all/builds"