import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.project_utils import get_url

def create_freestyle_item(browser, wait2, item_name, save=True):
    new_item_link = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item_link.click()

    name_field = wait2.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys(item_name)

    freestyle_option = browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    )
    freestyle_option.click()

    ok_button = browser.find_element(By.ID, "ok-button")
    ok_button.click()

    if save:
        save_button = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='Submit'][value='Save']")))
        save_button.click()

def test_duplicate_option_reveals_copy_from_field(browser, wait2, wait10):
    create_freestyle_item(browser, wait2, "FirstTestItem")

    wait10.until(EC.url_contains("/job/"))

    browser.get(get_url())

    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    duplicate_option = wait2.until(EC.element_to_be_clickable((By.ID, "duplicate-job")))
    assert duplicate_option.is_displayed()

    browser.execute_script("arguments[0].scrollIntoView(true);", duplicate_option)
    duplicate_option.click()

    from_field = wait2.until(EC.visibility_of_element_located((By.ID, "from")))
    assert from_field.is_displayed()

def test_created_item_visible_on_dashboard(browser, wait2, wait10):
    create_freestyle_item(browser, wait2, "DashboardVisibilityItem")

    wait10.until(EC.url_contains("/job/"))

    browser.get(get_url())

    item_link = browser.find_element(By.CSS_SELECTOR, "a[href='job/DashboardVisibilityItem/']")
    assert item_link.is_displayed()
    assert item_link.text == "DashboardVisibilityItem"