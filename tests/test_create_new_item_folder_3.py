
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_create_item_folder(browser):
    new_item = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()
    assert browser.current_url == 'http://localhost:8080/view/all/newJob'
    name_new_item = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']")))
    name_new_item.send_keys("folder_name")
    assert browser.find_element(By.XPATH, "//input[@id='name']").get_attribute('value') == "folder_name"
    folder_link = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Folder']")))
    folder_link.click()
    btn_ok = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ok-button']")))
    btn_ok.click()
    configuration = WebDriverWait(browser,5).until(EC.visibility_of_element_located((By.XPATH, "//h1")))
    assert configuration.is_displayed()
    display_name_fild = WebDriverWait(browser,2).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='_.displayNameOrNull']")))
    display_name_fild.send_keys("Display")
    discrip_filde = WebDriverWait(browser,2).until(EC.visibility_of_element_located((By.XPATH,"//textarea[@name='_.description']")))
    discrip_filde.send_keys("Description hello world")
    btn_save = browser.find_element(By.XPATH, "//button[@value='Save']")
    btn_save.click()
    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()
