import secrets
import pytest

from pages.home_page import HomePage
from pages.multibranch_configuration_page import MultibranchConfigurationPage

PIPELINE_NAME = "Pipeline_1"


@pytest.fixture
def created_multibranch_pipeline(browser):
    (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PIPELINE_NAME)
        .select_multibranch_and_click_ok()
        .goto_home_page()
    )
    return PIPELINE_NAME


def test_create_multibranch_pipeline(browser, created_multibranch_pipeline):
    pipeline_name = created_multibranch_pipeline
    assert PIPELINE_NAME == pipeline_name


def test_return_to_the_dashboard_without_creating_multibranch_pipeline(browser):
    page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PIPELINE_NAME)
        .select_multibranch()
        .goto_home_page()
    )

    welcome_title = page.get_welcome_title()
    assert welcome_title == "Welcome to Jenkins!"


def test_multibranch_with_special_characters(browser):
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    pipeline_name = "Pipeline" + spec_char

    page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(pipeline_name)
        .select_multibranch()
    )

    escaped_char = (spec_char.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))
    expected_text = f"‘{escaped_char}’ is an unsafe character"

    assert page.is_ok_button_disabled()
    assert page.get_error_name_message() == expected_text


def test_rename_multibranch_pipeline_from_dropdown_menu(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline
    new_name = "Pipeline_2"

    item_page = (
        HomePage(browser)
        .click_project_context_menu_and_click_rename(project_name)
        .rename_to(new_name)
    )

    assert item_page.get_item_name() == new_name
    assert f"job/{new_name}" in browser.current_url


def test_rename_multibranch_pipeline_from_project_menu(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline
    new_name = "Pipeline_2"

    item_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_rename()
        .rename_to(new_name)
    )

    assert item_page.get_item_name() == new_name
    assert f"job/{new_name}" in browser.current_url


def test_rename_multibranch_pipeline_with_same_name(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    error_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_rename()
        .try_rename_to(project_name)
    )

    expected_text = "The new name is the same as the current name."
    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text


def test_rename_multibranch_pipeline_with_blank_name(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    error_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_rename()
        .try_rename_to()
    )

    expected_text = "No name is specified"
    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text


def test_rename_multibranch_pipeline_with_unsupported_characters(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)

    error_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_rename()
        .try_rename_to("Pipeline" + spec_char)
    )

    escaped_char = (spec_char.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))
    expected_text = f"‘{escaped_char}’ is an unsafe character"

    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text


def test_availability_of_health_metrics(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    configuration_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_configure(MultibranchConfigurationPage)
        .open_health_metrics_dropdown()
    )

    available_metrics = configuration_page.get_available_health_metrics()

    expected_metrics = ["Child item with the given name",
                        "Child item with worst health",
                        "Health of the primary branch of a repository"]

    for metric in expected_metrics:
        assert metric in available_metrics


def test_health_metrics_child_item_with_given_name(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    configuration_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_configure(MultibranchConfigurationPage)
        .expand_health_metrics()
        .open_metrics_dropdown()
        .select_health_metric("Child item with the given name")
    )

    assert configuration_page.is_child_name_input_displayed()


def test_health_metrics_child_item_with_worst_health(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    configuration_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_configure(MultibranchConfigurationPage)
        .expand_health_metrics()
        .open_metrics_dropdown()
        .select_health_metric("Child item with worst health")
    )

    assert configuration_page.is_recursive_checkbox_displayed()
    assert configuration_page.is_recursive_checkbox_selected()


def test_health_metrics_health_of_the_primary_branch(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    configuration_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_configure(MultibranchConfigurationPage)
        .expand_health_metrics()
        .open_metrics_dropdown()
        .select_health_metric("Health of the primary branch of a repository")
    )

    assert configuration_page.is_primary_branch_metric_displayed()


def test_all_health_metrics_are_added(browser, wait5, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    configuration_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_configure(MultibranchConfigurationPage)
        .expand_health_metrics()
        .open_metrics_dropdown()
        .select_health_metric("Child item with the given name")
        .open_metrics_dropdown()
        .select_health_metric("Child item with worst health")
        .open_metrics_dropdown()
        .select_health_metric("Health of the primary branch of a repository")
    )

    assert not configuration_page.is_add_metric_btn_enabled()


def test_delete_multibranch_pipeline_via_side_panel(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    home_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_delete()
        .confirm_delete_modal()
    )

    assert not home_page.is_project_present(project_name)


def test_cancel_pipeline_deletion(browser, created_multibranch_pipeline):
    project_name = created_multibranch_pipeline

    item_page = (
        HomePage(browser)
        .click_job(project_name)
        .click_delete()
        .cancel_delete_modal()
    )

    assert item_page.get_item_name() == project_name
    assert f"job/{project_name}/" in browser.current_url
