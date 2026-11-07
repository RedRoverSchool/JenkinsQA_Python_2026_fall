import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.skip
def test_access_enable_disable_option(browser):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "a[href='/']").click()
    browser.find_element(By.CSS_SELECTOR, "button.jenkins-menu-dropdown-chevron").click()

    browser.find_element(By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']").click()
    enable_disable_option = browser.find_element(By.ID, "enable-disable-project")

    assert f"/job/{project_name}/configure" in browser.current_url
    assert project_name in browser.find_element(By.TAG_NAME, "body").text
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

    old_body = browser.find_element(By.TAG_NAME, "body")

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']").click()

    WebDriverWait(browser, 10).until(EC.staleness_of(old_body))

    assert "This project is currently disabled" not in browser.find_element(By.TAG_NAME, "body").text
    assert len(browser.find_elements(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")) == 0


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


def test_environment_options_are_available(browser):
    project_name = "Freestyle_Environment_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Environment']]").click()

    delete_workspace = browser.find_element(By.XPATH, "//label[normalize-space()='Delete workspace before build starts']")
    secret_text = browser.find_element(By.XPATH, "//label[normalize-space()='Use secret text(s) or file(s)']")
    timestamps = browser.find_element(By.XPATH, "//label[normalize-space()='Add timestamps to the Console Output']")
    build_scans = browser.find_element(By.XPATH, "//label[normalize-space()='Inspect build log for published build scans']")
    terminate_build = browser.find_element(By.XPATH, "//label[normalize-space()=\"Terminate a build if it's stuck\"]")
    ant = browser.find_element(By.XPATH, "//label[normalize-space()='With Ant']")

    assert delete_workspace.is_displayed()
    assert secret_text.is_displayed()
    assert timestamps.is_displayed()
    assert build_scans.is_displayed()
    assert terminate_build.is_displayed()
    assert ant.is_displayed()


def test_create_project_without_environment_settings(browser):
    project_name = "Freestyle_Environment_Default_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Environment']]").click()

    timestamps = browser.find_element(By.ID, "cb21")
    delete_workspace = browser.find_element(By.ID, "cb18")
    secret_text = browser.find_element(By.ID, "cb19")
    build_scans = browser.find_element(By.ID, "cb22")
    terminate_build = browser.find_element(By.ID, "cb23")
    ant = browser.find_element(By.NAME, "hudson-tasks-AntWrapper")

    assert not timestamps.is_selected()
    assert not delete_workspace.is_selected()
    assert not secret_text.is_selected()
    assert not build_scans.is_selected()
    assert not terminate_build.is_selected()
    assert not ant.is_selected()

