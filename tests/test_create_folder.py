from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_folder_and_checking_if_the_folder_was_created(browser):
    FOLDER_NAME = f"Folder_{random.randint(0,1000)}"
    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    # input_name_field = browser.find_element(By.XPATH, "//input[@name='name']")
    # input_name_field.send_keys(FOLDER_NAME)

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    browser.find_element(By.XPATH, "//input[@name='name']").send_keys(FOLDER_NAME)

    # folder_type_of_field = browser.find_element(By.XPATH, "//span[text()='Folder']")
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()='Folder']"))
    )
    # folder_type_of_field.click()
    browser.find_element(By.XPATH, "//span[text()='Folder']").click()

    # ok_button = browser.find_element(By.ID, "ok-button")
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "ok-button"))
    )
    browser.find_element(By.ID, "ok-button").click()

    # submit_button = browser.find_element(By.XPATH, "//button[@name='Submit']")
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )
    browser.find_element(By.NAME, "Submit").click()

    # jenkins_dashboard = browser.find_element(By.XPATH, "//span[text()='Jenkins']")
    # WebDriverWait(browser, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, "//span[text()='Jenkins']"))
    # )
    #
    # browser.find_element(By.XPATH, "//span[text()='Jenkins']").click()

    jenkins_logo = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo"))
    )
    browser.execute_script("arguments[0].click();", jenkins_logo)

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    # created_folder = browser.find_element(By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']")
    # assert browser.find_element(By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']").is_displayed()

    assert WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[normalize-space(.) = '{FOLDER_NAME}']"))
    )








