import pytest
from pages.folder_configuration_page import FolderConfigurationPage
from pages.home_page import HomePage

ORGANIZATION_FOLDER_NAME = "Organization_Folder_Config_Test"
DISPLAY_NAME = "Organization Folder Display Name"
DESCRIPTION_TEXT = "Organization Folder Description"

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

@pytest.mark.dependency(depends=["organization_folder_created"])
def test_edit_organization_folder_display_name_and_description(browser):
    configuration_page = (
        HomePage(browser)
        .click_job(ORGANIZATION_FOLDER_NAME)
        .click_configure(FolderConfigurationPage)
        .set_display_name(DISPLAY_NAME)
        .set_dicription(DESCRIPTION_TEXT)
    )

    assert configuration_page.get_display_name() == DISPLAY_NAME
    assert configuration_page.get_description() == DESCRIPTION_TEXT

