from selenium.webdriver.common.by import By


def test_item_with_invalid_special_characters(browser):
    item_name = "Test/Item"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    error_message = browser.find_element(By.CLASS_NAME, "error")
    assert error_message.text == "‘/’ is an unsafe character"

    ok_button = browser.find_element(By.ID, "ok-button")
    assert ok_button.get_attribute("disabled") is not None

    assert "/view/all/newJob" in browser.current_url
