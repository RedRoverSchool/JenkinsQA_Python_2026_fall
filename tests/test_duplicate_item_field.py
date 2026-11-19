import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from common.project_utils import get_url

def create_freestyle_item(browser, wait2, wait10, item_name, save=True):
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
        save_button = wait2.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[name='Submit'][value='Save']")
            )
        )
        save_button.click()

        wait10.until(
            EC.url_contains(f"/job/{item_name}/")
        )

def click_when_fresh(locator):
    def click(driver):
        try:
            element = EC.element_to_be_clickable(locator)(driver)
            if not element:
                return False
            element.click()
            return True
        except StaleElementReferenceException:
            return False
    return click

def return_to_dashboard(browser, wait10):
    wait10.until(
        click_when_fresh(
            (By.CSS_SELECTOR, "a.app-jenkins-logo")
        )
    )
    wait10.until(EC.url_to_be(get_url()))


def test_duplicate_option_reveals_copy_from_field(browser, wait2, wait10):
    create_freestyle_item(browser, wait2, wait10, "FirstTestItem")

    return_to_dashboard(browser, wait10)

    wait10.until(
        click_when_fresh(
            (By.CSS_SELECTOR, "a[href='/view/all/newJob']")
        )
    )

    duplicate_option = wait10.until(
        EC.visibility_of_element_located((By.ID, "duplicate-job"))
    )
    assert duplicate_option.is_displayed()

    browser.execute_script("arguments[0].scrollIntoView(true);", duplicate_option)

    wait10.until(
        click_when_fresh((By.ID, "duplicate-job"))
    )

    from_field = wait10.until(EC.visibility_of_element_located((By.ID, "from")))
    assert from_field.is_displayed()

def test_created_item_visible_on_dashboard(browser, wait2, wait10):
    item_name = "DashboardVisibilityItem"

    create_freestyle_item(browser, wait2, wait10, item_name)

    return_to_dashboard(browser, wait10)

    item_link = wait10.until(
        EC.visibility_of_element_located(
            (By.LINK_TEXT, item_name)
        )
    )

    assert item_link.is_displayed()

def test_item_visible_after_skipping_save(browser, wait2, wait10):
    item_name = "SkipSaveItem"

    create_freestyle_item(browser, wait2, wait10, item_name, save=False)

    return_to_dashboard(browser, wait10)

    item_link = wait10.until(
        EC.visibility_of_element_located((By.LINK_TEXT, item_name))
    )
    assert item_link.is_displayed()
