from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest


def test_open_page(browser, wait10):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    wait10.until(EC.visibility_of_element_located((By.ID, "name")))

    items_type_list = browser.find_element(By.ID, "items")
    pipeline_item = browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    pipeline_label = pipeline_item.find_element(By.CLASS_NAME, "jenkins-choice-list__item__label")

    assert "/view/all/newJob" in browser.current_url
    assert items_type_list.is_displayed()
    assert pipeline_item.is_displayed()
    assert pipeline_label.text == "Pipeline"


def test_validate_blank_name(browser, wait10):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    name_field = wait10.until(EC.visibility_of_element_located((By.ID, "name")))

    ok_button = browser.find_element(By.ID, "ok-button")

    assert "/view/all/newJob" in browser.current_url
    assert name_field.get_attribute("value") == ""
    assert not ok_button.is_enabled()


def test_validate_invalid_characters(browser, wait10):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    name_field = wait10.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys("Test")

    wait10.until(EC.text_to_be_present_in_element_attribute((By.ID, "name"),"data-valid","true"))
    name_field.send_keys("?")

    error_message = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".validation-error-area--visible .error")))

    ok_button = browser.find_element(By.ID, "ok-button")

    assert "/view/all/newJob" in browser.current_url
    assert error_message.text == "‘?’ is an unsafe character"
    assert not ok_button.is_enabled()


def test_create_with_valid_unique_name(browser, wait10):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    name_field = wait10.until(EC.visibility_of_element_located((By.ID, "name")))
    item_name = "TestJob"
    name_field.send_keys(item_name)

    pipeline_item = browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    pipeline_item.click()

    ok_button = browser.find_element(By.ID, "ok-button")
    ok_button.click()

    wait10.until(EC.url_contains(f"/job/{item_name}/configure"))


def test_validate_existing_name(browser, wait10):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    item_name = "TestJob"

    name_field = wait10.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys(item_name)

    browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob").click()
    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{item_name}/configure"))

    browser.find_element(By.CLASS_NAME, "app-jenkins-logo").click()
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    name_field = wait10.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys(item_name)

    browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob").click()

    error_locator = (By.CSS_SELECTOR, ".validation-error-area .error")
    error_text = f"A job already exists with the name ‘{item_name}’"

    WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element(error_locator, error_text))

    error_message = browser.find_element(By.CSS_SELECTOR, ".validation-error-area .error")
    ok_button = browser.find_element(By.ID, "ok-button")

    assert error_message.text == error_text
    assert not ok_button.is_enabled()