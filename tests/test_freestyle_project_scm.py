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