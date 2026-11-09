from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.project_utils import get_url


def test_duplicate_option_reveals_copy_from_field(browser, wait2):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    name_field = wait2.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys("FirstTestItem")

    freestyle_option = browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    )
    freestyle_option.click()

    ok_button = browser.find_element(By.ID, "ok-button")
    ok_button.click()

    save_button = wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='Submit'][value='Save']")))
    save_button.click()

    browser.get(get_url())

    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()

    duplicate_option = wait2.until(EC.element_to_be_clickable((By.ID, "duplicate-job")))
    assert duplicate_option.is_displayed()

    browser.execute_script("arguments[0].scrollIntoView(true);", duplicate_option)
    duplicate_option.click()

    from_field = wait2.until(EC.visibility_of_element_located((By.ID, "from")))
    assert from_field.is_displayed()