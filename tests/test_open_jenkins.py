
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import wait5

@pytest.mark.dependency()
def test_open_jenkins(browser):
    label = browser.find_element(By.XPATH, "//h1[text()='Welcome to Jenkins!']")
    assert label.text == "Welcome to Jenkins!"

@pytest.mark.dependency(depends=["test_open_jenkins"])
def test_new_item_page_open(browser):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    label_new_item = browser.find_element(By.XPATH, "//h1")
    assert label_new_item.is_displayed()


@pytest.mark.dependency(depends=["test_new_item_page_open"])
def test_create_new_folder(browser,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_name_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']")))
    item_name_fild.send_keys("folder_name")
    item_type_folder = browser.find_element(By.XPATH,"//span[text()='Folder']")
    item_type_folder.click()
    wait5.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']"))).click()
    display_name = wait5.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='_.displayNameOrNull']")))
    display_name.send_keys("Display")
    disc_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='_.description']")))
    disc_fild.send_keys("Description hello world")
    browser.find_element(By.XPATH, "//button[@value='Save']").click()
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()


def test_open_builds_history(browser,wait5,wait10):
    builds_history_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/builds']")
    builds_history_link.click()
    title = browser.find_element(By.XPATH, "//h1")
    assert title.is_displayed()


def test_create_job_with_out_display_name_and_discription(browser,wait5,wait10):
    new_job_link = browser.find_element(By.XPATH,"//span[text()='Create a job']")
    new_job_link.click()
    job_name_fild = wait5.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='name']")))
    job_name_fild.send_keys("Jobname")
    item_type_folder = wait5.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Folder']")))
    item_type_folder.click()
    button_ok = browser.find_element(By.XPATH, "//button[@id='ok-button']")
    button_ok.click()
    button_save = browser.find_element(By.XPATH, "//button[@value='Save']")
    button_save.click()
    titel = browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']")
    assert titel.is_displayed()