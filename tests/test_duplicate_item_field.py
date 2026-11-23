import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from common.project_utils import get_url
from pages.home_page import HomePage

def test_duplicate_option_reveals_copy_from_field(browser):
    item_name = "FirstTestItem"

    new_item_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_freestyle_and_click_ok()
        .click_save()
        .goto_home_page()
        .click_new_item()
    )

    assert new_item_page.is_duplicate_option_displayed()

    new_item_page.click_duplicate_option()

    assert new_item_page.is_from_field_displayed()

def test_created_item_visible_on_dashboard(browser):
    item_name = "DashboardVisibilityItem"

    home_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_freestyle_and_click_ok()
        .click_save()
        .goto_home_page()
    )

    assert home_page.is_project_displayed(item_name)

def test_item_visible_after_skipping_save(browser):
    item_name = "SkipSaveItem"

    home_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_freestyle_and_click_ok()
        .goto_home_page()
    )
    assert home_page.is_project_displayed(item_name)

def test_successful_item_duplication(browser):
    source_name = "CopySourceItem"
    new_name = "CopiedItem"
    description_text = "Test description for copying"

    source_project_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(source_name)
        .select_freestyle_and_click_ok()
        .enter_description(description_text)
        .click_save()
    )

    new_project_config_page = (
        source_project_page
        .goto_home_page()
        .click_new_item()
        .set_item_name(new_name)
        .click_duplicate_option()
        .set_duplicate_item_name(source_name)
        .select_duplicate_item(source_name)
        .click_ok_expecting_success()
    )

    assert new_project_config_page.get_description() == description_text