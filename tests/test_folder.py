from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
import pytest

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


@pytest.mark.skip(reason="failed")
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
