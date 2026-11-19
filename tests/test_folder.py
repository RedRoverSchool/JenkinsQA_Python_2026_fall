import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage


def test_create_folder_from_dashboard(browser, wait10):

    folder_name = "TestFolder_01"

    project_name=(
        HomePage(browser.driver)
        .click_new_item()
        .set_item_name(folder_name)
        .select_folder_and_click_ok()
        .goto_home_page()
        .get_first_project_name())

    assert folder_name in project_name


def test_create_nested_folder(browser, wait10):

    parent_name = "ParentFolder2"
    child_name = "NestedFolder2"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(parent_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.visibility_of_element_located((By.NAME, "Submit"))).click()
    wait10.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), parent_name))

    new_item_btn = wait10.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'newJob')]")))
    new_item_btn.click()
    wait10.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys(child_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()
    wait10.until(EC.visibility_of_element_located((By.NAME, "Submit"))).click()

    wait10.until(EC.presence_of_element_located((By.CLASS_NAME, "jenkins-breadcrumbs__list")))
    breadcrumbs_text = browser.find_element(By.CLASS_NAME, "jenkins-breadcrumbs__list").text

    assert parent_name in breadcrumbs_text
    assert child_name in breadcrumbs_text
