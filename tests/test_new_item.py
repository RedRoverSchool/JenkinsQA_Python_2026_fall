from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_item_with_blank_name(browser):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    assert "/view/all/newJob" in browser.current_url

    assert browser.find_element(By.ID, "name").is_displayed()
    assert browser.find_element(By.ID, "name").get_attribute("value") == ""

    browser.find_element(
        By.CSS_SELECTOR,
        "input[value='hudson.model.FreeStyleProject'] + span"
    ).click()

    name_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    assert name_field.is_displayed()


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

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    ).click()

    WebDriverWait(browser, 10).until(
        EC.url_contains(f"/job/{item_name}/")
    )

    assert item_name in browser.current_url


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


def test_item_with_invalid_special_characters(browser):
    item_name = "Test/Item"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    browser.find_element(By.ID, "name").send_keys(item_name)

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    error_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error"))
    )
    assert error_message.text == "‘/’ is an unsafe character"

    ok_button = browser.find_element(By.ID, "ok-button")
    assert ok_button.get_attribute("disabled") is not None

    assert "/view/all/newJob" in browser.current_url


def test_return_to_dashboard(browser):
    browser.find_element(By.LINK_TEXT, "New Item").click()

    browser.find_element(By.ID, "name").send_keys("Dashboard_Return_Test")

    browser.find_element(
        By.CSS_SELECTOR,
        "label:has(input[value='hudson.model.FreeStyleProject'])"
    ).click()

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    ).click()

    WebDriverWait(browser, 10).until(
        EC.url_contains("/job/Dashboard_Return_Test/")
    )

    project_url = browser.current_url

    browser.find_element(
        By.XPATH, "//span[text()='Jenkins']"
    ).click()

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