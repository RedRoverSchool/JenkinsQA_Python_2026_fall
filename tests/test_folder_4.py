import pytest
from selenium.webdriver.common.bidi import browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import wait5


def test_create_item_folder(browser,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_name_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']")))
    item_name_fild.send_keys("folder_name")
    item_type_folder = browser.find_element(By.XPATH, "//span[text()='Folder']")
    item_type_folder.click()
    wait5.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']"))).click()
    display_name = wait5.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='_.displayNameOrNull']")))
    display_name.send_keys("Display")
    disc_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='_.description']")))
    disc_fild.send_keys("Description hello world")
    browser.find_element(By.XPATH, "//button[@value='Save']").click()
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()


def test_create_item_folder_with_empty_name(browser,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_type_folder = browser.find_element(By.XPATH, "//span[text()='Folder']")
    item_type_folder.click()
    button_ok = browser.find_element(By.XPATH, "//button[@id='ok-button']")
    assert not button_ok.is_enabled()


@pytest.mark.parametrize('invalid_characters',['/','!','?','&','*','>'])
def test_create_item_folder_with_empty_invalid_characters_in_name(browser,invalid_characters,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_name_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']")))
    item_name_fild.send_keys(invalid_characters)
    error = wait5.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='error']")))
    assert error.is_displayed()