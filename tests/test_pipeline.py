import string
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def test_create(browser):
    name_pipeline = ''.join(random.choices(string.ascii_lowercase, k=10))

    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys(name_pipeline)

    ok_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button")))
    ok_button.click()

    save_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@value = 'Save']")))
    save_button.click()

    assert WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[normalize-space(.) = '{name_pipeline}']"))
    )

def test_create_with_invalid_name(browser):
    wait = WebDriverWait(browser, 10)
    invalid_name = 'pap$line!'

    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys(invalid_name)

    error = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'error']"))
    )
    error_visible = error.is_displayed()

    button_disabled = wait.until(
        EC.element_attribute_to_include((By.ID, "ok-button"), "disabled")
    )

    assert error_visible and button_disabled

