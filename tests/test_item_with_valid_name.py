from selenium.webdriver.common.by import By


def test_create_item_with_valid_name(browser):
    item_name = "Test_Item_001"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    name_field = browser.find_element(By.ID, "name")
    assert name_field.is_enabled()

    name_field.send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    browser.find_element(By.ID, "ok-button").click()

    assert item_name in browser.current_url
