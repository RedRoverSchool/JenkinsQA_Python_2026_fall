from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest


def test_create_item_with_blank_name(browser, wait2):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    name_field = wait2.until( EC.visibility_of_element_located((By.ID, "name")) )
    browser.find_element( By.CSS_SELECTOR,"input[value='hudson.model.FreeStyleProject'] + span" ).click()

    assert "/view/all/newJob" in browser.current_url
    assert name_field.is_displayed()
    assert name_field.get_attribute("value") == ""


@pytest.mark.dependency(name="create_item")
def test_create_item_with_valid_name(browser, wait5):
    item_name = "Test_Item_001"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    name_field = browser.find_element(By.ID, "name")
    name_field_enabled = name_field.is_enabled()
    name_field.send_keys(item_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()

    wait5.until(EC.element_to_be_clickable((By.ID, "ok-button"))).click()
    wait5.until(EC.url_contains(f"/job/{item_name}/"))

    assert name_field_enabled
    assert item_name in browser.current_url


@pytest.mark.dependency(name="existing_item", depends=["create_item"])
def test_create_item_with_existing_name(browser, wait5):
    item_name = "Test_Item_001"

    browser.find_element(By.XPATH, "//span[text()='Jenkins']").click()

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()

    error_message = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'A job already exists')]"))
    )
    ok_button_enabled = browser.find_element(By.ID, "ok-button").is_enabled()

    assert item_name in error_message.text
    assert not ok_button_enabled


@pytest.mark.dependency(name="invalid_special_characters",depends=["existing_item"])
def test_item_with_invalid_special_characters(browser, wait5):
    item_name = "Test/Item"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()

    error_message = wait5.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error"))
    )

    ok_button_disabled = browser.find_element(By.ID, "ok-button").get_attribute("disabled")

    assert error_message.text == "‘/’ is an unsafe character"
    assert ok_button_disabled is not None
    assert "/view/all/newJob" in browser.current_url


@pytest.mark.dependency(depends=["invalid_special_characters"])
def test_return_to_dashboard(browser, wait5):
    project_name = "Test_Item_001"

    browser.find_element(By.XPATH, "//span[text()='Jenkins']").click()

    wait5.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), project_name)
    )

    dashboard_text = browser.find_element(By.TAG_NAME, "body").text

    assert project_name in dashboard_text