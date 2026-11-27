import pytest

from pages.home_page import HomePage

ORGANIZATION_FOLDER_NAME = "Organization_Folder_Config_Test"


@pytest.mark.dependency(name="organization_folder_created")
def test_create_organization_folder_and_access_general_settings(browser):
    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(ORGANIZATION_FOLDER_NAME)
        .select_organization_folder_and_click_ok()
    )

    first_general_displayed = configuration_page.is_general_section_displayed()

    home_page = configuration_page.goto_home_page()
    item_page = home_page.click_job(ORGANIZATION_FOLDER_NAME)
    configuration_page = item_page.click_configure()

    second_general_displayed = configuration_page.is_general_section_displayed()

    assert first_general_displayed
    assert second_general_displayed