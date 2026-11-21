import string
import random
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage

NAME_PIPELINE = ''.join(random.choices(string.ascii_lowercase, k=10))

@pytest.mark.dependency()
def test_create(browser):
    pipeline_name = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(NAME_PIPELINE)
        .select_pipeline_and_click_ok()
        .goto_home_page()
        .get_first_project_name()
    )

    assert NAME_PIPELINE in pipeline_name


def test_create_with_invalid_name(browser):
    invalid_name = 'pap$line!'

    new_item_page = (
        HomePage(browser)
        .click_new_item()
        .select_pipeline()
        .set_item_name(invalid_name)
    )

    assert new_item_page.is_error_message_displayed()
    assert new_item_page.is_ok_button_disabled()

def test_disable_the_project(browser):
    pipeline_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(NAME_PIPELINE)
        .select_pipeline_and_click_ok()
        .switch_button_disabled()
        .click_save()
    )

    assert pipeline_page.get_warning_message() == "This project is currently disabled"
    assert pipeline_page.is_enabled_button_visible()

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