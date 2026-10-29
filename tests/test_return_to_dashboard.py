from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_return_to_dashboard(browser):
    browser.find_element(By.LINK_TEXT, "New Item").click()
    browser.find_element(By.ID, "name").send_keys("Dashboard_Return_Test")
    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()
    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until(
        EC.url_contains("/job/Dashboard_Return_Test/")
    )

    project_url = browser.current_url

    browser.find_element(By.XPATH, "//span[text()='Jenkins']").click()

    WebDriverWait(browser, 10).until(
        EC.url_changes(project_url)
    )

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "Dashboard_Return_Test"
        )
    )

    assert "Dashboard_Return_Test" in browser.find_element(
        By.TAG_NAME, "body"
    ).text
