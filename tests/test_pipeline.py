import string
import random
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

NAME_PIPELINE = ''.join(random.choices(string.ascii_lowercase, k=10))

@pytest.mark.dependency()
def test_create(browser, wait5):
    create_item_button = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys(NAME_PIPELINE)

    ok_button = wait5.until(
        EC.element_to_be_clickable((By.ID, "ok-button")))
    ok_button.click()

    assert wait5.until(EC.url_contains(f"/job/{NAME_PIPELINE}/configure")
    )

def test_create_with_invalid_name(browser, wait2, wait5):
    invalid_name = 'pap$line!'

    create_item_button = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys(invalid_name)

    error = wait2.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'error']"))
    )
    error_visible = error.is_displayed()

    button_disabled = wait2.until(
        EC.element_attribute_to_include((By.ID, "ok-button"), "disabled")
    )

    assert error_visible and button_disabled

def test_disable_the_project(browser, wait5, wait2):
    name_pipeline = ''.join(random.choices(string.ascii_lowercase, k=10))

    create_item_button = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys(name_pipeline)

    ok_button = wait5.until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    ok_button.click()

    enabled_radiobutton = wait5.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class = 'jenkins-toggle-switch__label ']"))
    )
    enabled_radiobutton.click()

    save_button = wait2.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@value = 'Save']")))
    save_button.click()

    warning = wait5.until(
        EC.visibility_of_element_located((By.ID, "enable-project"))
    )
    text_warning = warning.text.split('\n')[0].strip()

    enabled_button = wait2.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button[value='Enable']"))
    )

    assert text_warning == "This project is currently disabled" and enabled_button.is_enabled()

@pytest.mark.dependency(depends = "test_create")
def test_rename_left_side(browser, wait5, wait2):
    wait5.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[href='job/{NAME_PIPELINE}/']"))).click()

    rename_button = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[href='/job/{NAME_PIPELINE}/confirm-rename']")))
    rename_button.click()

    new_name_pipeline = ''.join(random.choices(string.ascii_lowercase, k=10))
    name_field = browser.find_element(By.CSS_SELECTOR, "[name='newName']")

    name_field.clear()
    name_field.send_keys(new_name_pipeline)

    browser.find_element(By.CSS_SELECTOR, "[name='Submit']").click()
    actual_name = wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".job-index-headline"))).text

    assert actual_name == new_name_pipeline