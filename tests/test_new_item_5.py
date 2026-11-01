from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_cannot_create_item_with_empty_name(browser):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    assert "/view/all/newJob" in browser.current_url

    name_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )

    assert name_field.is_displayed()
    assert name_field.get_attribute("value") == ""

    browser.find_element(
        By.CSS_SELECTOR,
        "input[value='com.cloudbees.hudson.plugins.folder.Folder'] + span"
    ).click()

    ok_button = browser.find_element(By.ID, "ok-button")

    assert not ok_button.is_enabled()