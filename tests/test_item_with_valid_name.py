import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

@pytest.mark.skip
def test_create_item_with_valid_name(browser):
    item_name = "Test_Item_001"

    browser.find_element(
        By.CSS_SELECTOR,
        "a[href='/view/all/newJob']"
    ).click()

    name_field = browser.find_element(By.ID, "name")
    assert name_field.is_enabled()

    name_field.send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until(
        lambda driver: driver.find_element(By.TAG_NAME, "body")
    )

    print("Current URL:", browser.current_url)
    print("Page text:", browser.find_element(By.TAG_NAME, "body").text)

    assert item_name in browser.current_url