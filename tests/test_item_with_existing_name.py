from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_item_with_existing_name(browser):
    wait = WebDriverWait(browser, 10)
    item_name = "Existing_Item"

    browser.find_element(
        By.CSS_SELECTOR, "a[href='/view/all/newJob']"
    ).click()

    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    ).click()

    wait.until(
        EC.url_contains("/job/Existing_Item/")
    )

    wait.until(
        EC.element_to_be_clickable((By.ID, "jenkins-head-icon"))
    ).click()

    browser.find_element(
        By.CSS_SELECTOR, "a[href='/view/all/newJob']"
    ).click()

    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    error_message = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'A job already exists')]")
        )
    )

    assert item_name in error_message.text

    ok_button = browser.find_element(By.ID, "ok-button")
    assert not ok_button.is_enabled()
