import pytest
from pages.home_page import HomePage
from pages.pipeline_configuration_page import PipelineConfigurationPage


def test_open_page(browser):
    new_item_page = HomePage(browser).click_new_item()

    assert new_item_page.is_items_type_list_displayed()
    assert new_item_page.is_pipeline_displayed()
    assert new_item_page.get_pipeline_label() == "Pipeline"


def test_validate_blank_name(browser):
    new_item_page = (
        HomePage(browser)
        .click_new_item()
    )

    assert new_item_page.get_item_name() == ""
    assert new_item_page.is_ok_button_disabled()


def test_validate_invalid_characters(browser):
    item_name = "Test"

    new_item_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .wait_for_valid_item_name()
    )

    new_item_page.set_item_name("?")

    assert new_item_page.get_error_name_message() == "‘?’ is an unsafe character"
    assert new_item_page.is_ok_button_disabled()


@pytest.mark.dependency()
def test_create_with_valid_unique_name(browser):
    item_name = "TestJob"

    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_pipeline_and_click_ok()
    )

    assert configuration_page.is_configuration_page_opened(item_name)


def test_validate_existing_name(browser):
    item_name = "TestJob"
    error_text = f"A job already exists with the name ‘{item_name}’"

    (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_pipeline_and_click_ok()
        .goto_home_page()
    )

    new_item_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_pipeline()
    )

    assert new_item_page.get_error_name_message() == error_text
    assert new_item_page.is_ok_button_disabled()


@pytest.mark.dependency(depends=["test_create_with_valid_unique_name"])
def test_item_appears_on_dashboard(browser):
    item_name = "TestJob"

    dashboard = PipelineConfigurationPage(browser).goto_home_page()

    assert dashboard.is_project_displayed(item_name)