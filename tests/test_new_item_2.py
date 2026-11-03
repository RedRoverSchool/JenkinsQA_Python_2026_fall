from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid


def test_open_new_item_page(browser):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()
    assert "/view/all/newJob" in browser.current_url

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "name")))

    items_type_list = browser.find_element(By.ID, "items")
    assert items_type_list.is_displayed()

    pipeline_item = browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    pipeline_label = pipeline_item.find_element(By.CLASS_NAME, "jenkins-choice-list__item__label")
    assert pipeline_item.is_displayed() and pipeline_label.text == "Pipeline"


def test_validate_blank_name(browser):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()
    assert "/view/all/newJob" in browser.current_url

    name_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "name")))
    assert name_field.is_displayed()
    assert name_field.get_attribute("value") == ""

    ok_button = browser.find_element(By.ID, "ok-button")
    assert not ok_button.is_enabled()


def test_validate_invalid_characters(browser):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()
    assert "/view/all/newJob" in browser.current_url

    name_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys("Test?Job")

    error_message = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "error")))
    assert error_message.text == "‘?’ is an unsafe character"

    ok_button = browser.find_element(By.ID, "ok-button")
    assert not ok_button.is_enabled()


def test_create_item_with_valid_unique_name(browser):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()
    assert "/view/all/newJob" in browser.current_url

    name_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "name")))
    item_name = f"TestJob_{uuid.uuid4().hex[:8]}"
    name_field.send_keys(item_name)

    pipeline_item = browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    pipeline_item.click()

    ok_button = browser.find_element(By.ID, "ok-button")
    ok_button.click()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{item_name}/configure"))