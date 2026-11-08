import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_item_folder(browser):
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']"))).click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'

    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']"))).send_keys("folder_name")
    assert browser.find_element(By.XPATH, "//input[@id='name']").get_attribute('value') == "folder_name"

    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Folder']"))).click()
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']"))).click()

    assert WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH, "//h1"))).is_displayed()

    WebDriverWait(browser,5).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='_.displayNameOrNull']"))).send_keys("Display")

    WebDriverWait(browser,5).until(EC.visibility_of_element_located((By.XPATH,"//textarea[@name='_.description']"))).send_keys("Description hello world")

    browser.find_element(By.XPATH, "//button[@value='Save']").click()
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()
