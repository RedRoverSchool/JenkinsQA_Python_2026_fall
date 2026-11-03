from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def test_freestyle_tests(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()

    item_name = "Freestyle Project 1"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    wait = WebDriverWait(browser, 10)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[value='Save']")))
    save_button = browser.find_element(By.CSS_SELECTOR, "[value='Save']")
    save_button.click()

    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),item_name))

    assert item_name in browser.find_element(By.TAG_NAME, "h1").text



