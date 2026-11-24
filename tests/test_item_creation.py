import pytest
from pages.home_page import HomePage


PROJECT_NAME = "Test_Item_001"

@pytest.mark.dependency(name="item_created")
def test_create_item_with_valid_name(browser):
    home_page = HomePage(browser)
    new_item_page = home_page.click_new_item()

    name_field_enabled = new_item_page.is_item_name_enabled()
    new_item_page.set_item_name(PROJECT_NAME)
    new_item_page.select_freestyle_and_click_ok()

    assert name_field_enabled
    assert f"/job/{PROJECT_NAME}/" in browser.current_url


@pytest.mark.dependency(name="blank_name_checked", depends=["item_created"])
def test_item_with_blank_name(browser):
    home_page = HomePage(browser)
    new_item_page = home_page.click_new_item()

    new_item_page.select_freestyle()

    assert new_item_page.is_item_name_enabled()
    assert new_item_page.get_item_name() == ""
    assert "/view/all/newJob" in browser.current_url


@pytest.mark.dependency(name="existing_item_checked", depends=["blank_name_checked"])
def test_item_with_existing_name(browser):
    home_page = HomePage(browser)
    new_item_page = home_page.click_new_item()

    new_item_page.set_item_name(PROJECT_NAME)
    new_item_page.select_freestyle()

    error_message = new_item_page.get_error_name_message()
    ok_button_enabled = new_item_page.is_ok_button_enabled()

    assert PROJECT_NAME in error_message
    assert not ok_button_enabled


@pytest.mark.dependency(name="invalid_special_characters_checked", depends=["existing_item_checked"])
def test_item_with_invalid_special_characters(browser):
    home_page = HomePage(browser)
    new_item_page = home_page.click_new_item()

    new_item_page.set_item_name("Test/Item")
    new_item_page.select_freestyle()

    error_message = new_item_page.get_error_name_message()
    ok_button_disabled = new_item_page.is_ok_button_disabled()

    assert error_message == "‘/’ is an unsafe character"
    assert ok_button_disabled
    assert "/view/all/newJob" in browser.current_url


@pytest.mark.dependency(depends=["invalid_special_characters_checked"])
def test_return_to_dashboard(browser):
    home_page = HomePage(browser)
    dashboard = home_page.goto_home_page()

    assert dashboard.is_project_present(PROJECT_NAME)