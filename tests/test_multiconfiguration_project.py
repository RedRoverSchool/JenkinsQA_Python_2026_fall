import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages import multiconfiguration_configuration_page
from pages.home_page import HomePage

@pytest.mark.dependency()
def test_add_description_to_multiconfiguration_project(browser):

    project_name = "My multi-configuration project"
    description = "This is my multi-configuration project"

    multiconfiguration_project = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(project_name)
        .select_multiconfiguration_and_click_ok()
        .enter_description(description)
        .click_save()
    )

    assert multiconfiguration_project.get_description() == description


@pytest.mark.dependency(depends=["test_add_description_to_multiconfiguration_project"])
def test_verify_discard_old_builds_configuration_options(browser):

    project_name = "My multi-configuration project"
    days_to_keep = 7
    builds_to_keep = 20

    multiconfiguration_project = (
        HomePage(browser)
        .get_multiconfiguration_project(project_name)
        .get_configure()
        .enable_discard_old_builds()
        .set_days_to_keep(days_to_keep)
        .set_builds_to_keep(builds_to_keep)
        .click_save()
        .get_configure()
    )
    assert int(multiconfiguration_project.get_days_to_keep()) == days_to_keep
    assert int(multiconfiguration_project.get_builds_to_keep()) == builds_to_keep
    assert multiconfiguration_project.is_discard_old_builds_enabled()


@pytest.mark.dependency(depends=["test_add_description_to_multiconfiguration_project"])
def test_verify_github_project_configuration_options(browser):

    project_name = "My multi-configuration project"
    project_url = "https://github.com/tests/project/"

    multiconfiguration_project = (
        HomePage(browser)
        .get_multiconfiguration_project(project_name)
        .get_configure()
        .enable_github_project()
        .enter_project_url(project_url)
        .click_save()
        .get_configure()
    )
    assert multiconfiguration_project.get_project_url() == project_url
    assert multiconfiguration_project.is_github_project_enabled()


@pytest.mark.dependency(depends=["test_add_description_to_multiconfiguration_project"])
def test_verify_this_project_is_parameterised_configuration_options(browser):

    project_name = "My multi-configuration project"
    parameter_name = "TestParameter"
    default_value = "DefaultValue"
    parameter_description = "Test description"

    multiconfiguration_project = (
        HomePage(browser)
        .get_multiconfiguration_project(project_name)
        .get_configure()
        .enable_this_project_is_parameterised()
        .click_add_parameter()
        .select_string_parameter()
        .set_parameter_name(parameter_name)
        .set_default_value(default_value)
        .set_parameter_description(parameter_description)
        .click_save()
        .get_configure()
    )

    assert multiconfiguration_project.is_this_project_parameterised_enabled()
    assert multiconfiguration_project.get_parameter_name() == parameter_name
    assert multiconfiguration_project.get_default_value() == default_value
    assert multiconfiguration_project.get_parameter_description() == parameter_description


def test_verify_description_preview_can_be_displayed_and_hidden(browser):

    project_name = "My multi-configuration project"
    description = "This is a test description for my multi-configuration project"

    multiconfiguration_project = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(project_name)
        .select_multiconfiguration_and_click_ok()
        .enter_description(description)
        .click_preview()
    )

    assert multiconfiguration_project.is_preview_displayed()

    multiconfiguration_project.click_hide_preview()

    assert multiconfiguration_project.is_preview_hidden()