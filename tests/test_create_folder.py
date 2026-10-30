from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def test_create_folder_and_checking_if_the_folder_was_created(browser):
    wait = WebDriverWait(browser, 10)
    FOLDER_NAME = f"Folder_{random.randint(0,1000)}"
    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    input_name_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    input_name_field.send_keys(FOLDER_NAME)


    item_type_folder = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='Folder']"))
    )
    item_type_folder.click()

    ok_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "ok-button"))
    )
    ok_button.click()


    save_button = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )
    save_button.click()

    jenkins_logo = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo"))
    )
    browser.execute_script("arguments[0].click();", jenkins_logo)

    wait.until(
        EC.element_to_be_clickable((By.ID, "jenkins-head-icon"))
    ).click()
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[normalize-space(.) = '{FOLDER_NAME}']"))
    )








