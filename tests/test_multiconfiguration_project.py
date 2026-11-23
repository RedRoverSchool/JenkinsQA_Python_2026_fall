import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        .enter_description_and_click_save(description)
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



