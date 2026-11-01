import time

from selenium.webdriver.common.bidi import browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_open_jenkins(browser):
    label = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Welcome to Jenkins!']")))
    assert label.text == "Welcome to Jenkins!"


def test_new_item_page_open(browser):
    new_item = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'

def test_create_new_folder(browser):
    new_item = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']"))).click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'
    name_new_item = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']"))).send_keys("folder_name")
    assert browser.find_element(By.XPATH, "//input[@id='name']").get_attribute('value') == "folder_name"
    folder_link = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Folder']"))).click()
    btn_ok = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']"))).click()
    assert browser.find_element(By.XPATH, "(//div[@class='jenkins-app-bar__content'])[1]").is_displayed()
    display_name_fild = WebDriverWait(browser,2).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='_.displayNameOrNull']"))).send_keys("Display")
    discrip_filde = WebDriverWait(browser,2).until(EC.visibility_of_element_located((By.XPATH,"//textarea[@name='_.description']"))).send_keys("Description hello world")
    btn_save = browser.find_element(By.XPATH, "//button[@value='Save']").click()
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()


def test_open_builds_history(browser):
    builds_history_link = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/builds']")))
    builds_history_link.click()
    assert browser.current_url == "http://localhost:8080/view/all/builds"


def test_create_new_job(browser):
    new_job_link = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Create a job']"))).click()
    assert browser.current_url == 'http://localhost:8080/newJob'
    job_name_fild = WebDriverWait(browser,3).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='name']")))
    job_name_fild.send_keys("Jobname")
    name = job_name_fild.get_attribute('value')
    item_type = WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Folder']")))
    item_type.click()
    btn_ok = WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']"))).click()
    assert browser.find_element(By.XPATH,"//span[text()='Configuration']").is_displayed()
    btn_save = WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.XPATH, "//button[@value='Save']"))).click()
    WebDriverWait(browser,2).until(EC.url_to_be(f'http://localhost:8080/job/{name}/'))
    assert browser.current_url == f'http://localhost:8080/job/{name}/'