from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_freestyle_project_and_check_scm_types(browser):
    project_name = "Freestyle_SCM_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])" ).click()

    freestyle_selected = browser.find_element(By.CSS_SELECTOR, "input[value='hudson.model.FreeStyleProject']" ).is_selected()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/") )

    assert freestyle_selected
    assert browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Source Code Management']]").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-0']").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").is_displayed()
    assert browser.find_element(By.ID, "radio-block-0").is_selected()


def test_git_scm_fields_are_displayed_when_git_is_selected(browser):
    project_name = "Freestyle_Git_SCM_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element( By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])" ).click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until( EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.XPATH,"//button[.//span[normalize-space()='Source Code Management']]" ).click()

    browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='_.url']")
        )
 )

    credentials = browser.find_element( By.CSS_SELECTOR, "select[name='_.credentialsId']")

    branch = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='_.name'][default='*/master']")
        )
    )

    assert repository_url.is_displayed()
    assert credentials.is_displayed()
    assert branch.is_displayed()


def test_error_message_for_invalid_git_repository_url(browser):
    project_name = "Freestyle_Invalid_Git_URL_Test"
    invalid_repository_url = "https://github.com/invalid-user/non-existing-repository.git"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR,"label:has(input[value='hudson.model.FreeStyleProject'])").click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element( By.XPATH,"//button[.//span[normalize-space()='Source Code Management']]").click()

    browser.find_element( By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='_.url']")
        )
    )

    repository_url_field.send_keys(invalid_repository_url)

    repository_url_field.send_keys(Keys.TAB)

    error_message = WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((
            By.XPATH,
            "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"
        ), "Failed to connect to repository")
    )

    assert "Failed to connect to repository" in error_message.text