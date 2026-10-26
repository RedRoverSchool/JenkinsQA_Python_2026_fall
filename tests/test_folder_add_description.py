import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_description_to_folder(browser):

    folder_name = f"Test_folder_{random.randint(0, 999999)}"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(folder_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), folder_name))

    browser.find_element(By.XPATH, "//a[normalize-space()='Add description']").click()

    textarea = browser.find_element(By.CSS_SELECTOR, "textarea[name='description']")
    textarea.send_keys("Test description")

    assert textarea.get_attribute("value") == "Test description"