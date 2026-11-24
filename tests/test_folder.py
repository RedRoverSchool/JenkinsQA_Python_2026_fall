import pytest
from selenium.webdriver.common.keys import Keys

from pages.home_page import HomePage

FOLDER_NAME = "TestFolder_01"

def test_create_folder_from_dashboard(browser, wait10):
    folder_name = "TestFolder_01"

    project_name = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(folder_name)
        .select_folder_and_click_ok()
        .goto_home_page()
        .get_first_project_name()
    )

    assert folder_name in project_name


def test_create_nested_folder(browser, wait10):
    parent_name = "ParentFolder2"
    child_name = "NestedFolder2"

    breadcrumbs_text = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(parent_name)
        .select_folder_and_click_ok()
        .click_submit()
        .click_new_item()
        .set_item_name(child_name)
        .select_folder_and_click_ok()
        .click_submit()
        .get_breadcrumbs_text()
    )

    assert parent_name in breadcrumbs_text
    assert child_name in breadcrumbs_text


def test_create_folder_with_empty_name(browser):
    ok_button_enabled = (
    HomePage(browser)
    .click_new_item()
    .select_folder()
    .is_ok_button_enabled()
    )

    assert not ok_button_enabled


def test_create_folder_with_empty_name_error(browser):
    new_item_page = (
    HomePage(browser)
    .click_new_item()
    .set_item_name(FOLDER_NAME)
    .select_folder()
    .clear_item_name()
    .set_item_name(Keys.TAB)
    )

    error_message = new_item_page.get_error_name_message()

    assert any(word in error_message for word in ('пуст', 'empty'))
    assert not new_item_page.is_ok_button_enabled()


@pytest.mark.parametrize("symbols", ['A', 'ф', '1', 'te st', ' test ', ',', '"', "'"])
def test_folder_name_is_valid(browser, symbols):
    item_name_valid = (
    HomePage(browser)
    .click_new_item()
    .set_item_name(symbols)
    .is_item_name_valid()
    )

    assert item_name_valid


@pytest.mark.parametrize("symbols", ['/', '\\', '?', '*', ':', '|', '>', '<', '!', '&'])
def test_name_is_invalid(browser, symbols):
    item_name_valid = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(symbols)
        .is_item_name_valid()
    )

    assert not item_name_valid