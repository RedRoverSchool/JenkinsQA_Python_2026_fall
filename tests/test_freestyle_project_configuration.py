import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_access_enable_disable_option(browser):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(
        By.CSS_SELECTOR, "a[href='/view/all/newJob']"
    ).click()

    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(
        By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label"
    ).click()

    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(
        EC.url_contains(f"/job/{project_name}/")
    )

    assert f"/job/{project_name}/configure" in browser.current_url
    assert project_name in browser.find_element(By.TAG_NAME, "body").text

    browser.find_element(
        By.CSS_SELECTOR, "a[href='/']"
    ).click()

    browser.find_element(
        By.CSS_SELECTOR, "button.jenkins-menu-dropdown-chevron"
    ).click()

    browser.find_element(
        By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']"
    ).click()

    enable_disable_option = browser.find_element(
        By.ID, "enable-disable-project"
    )

    assert enable_disable_option.is_displayed()
    assert enable_disable_option.is_selected()


def test_disable_freestyle_project(browser):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()

    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "label[for='enable-disable-project']").click()

    browser.find_element( By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    WebDriverWait(browser, 10).until( EC.url_to_be(f"http://localhost:8080/job/{project_name}/"))

    assert "This project is currently disabled" in browser.find_element(By.TAG_NAME, "body").text

@pytest.mark.skip
def test_enable_disabled_freestyle_project(browser):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "label[for='enable-disable-project']").click()
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    WebDriverWait(browser, 10).until(EC.url_to_be(f"http://localhost:8080/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']").click()

    WebDriverWait(browser, 10).until(EC.url_to_be(f"http://localhost:8080/job/{project_name}/"))

    assert "This project is currently disabled" not in browser.find_element(By.TAG_NAME, "body").text


def test_save_freestyle_project_disabled_state(browser):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "label[for='enable-disable-project']").click()
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    WebDriverWait(browser, 10).until(EC.url_to_be(f"http://localhost:8080/job/{project_name}/"))

    browser.refresh()

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "This project is currently disabled"
        )
    )

    assert "This project is currently disabled" in browser.find_element(By.TAG_NAME, "body").text
    assert browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']").is_displayed()