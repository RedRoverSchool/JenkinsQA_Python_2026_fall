from selenium.webdriver.common.by import By

def test_create_item_with_blank_name(browser):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    assert "/view/all/newJob" in browser.current_url

    assert browser.find_element(By.ID, "name").is_displayed()
    assert browser.find_element(By.ID, "name").get_attribute("value") == ""

    browser.find_element(
        By.CSS_SELECTOR,
        "input[value='hudson.model.FreeStyleProject'] + span"
    ).click()

    assert not browser.find_element(By.ID, "ok-button").is_enabled()