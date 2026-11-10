import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.skip
@pytest.mark.dependency(name="project_created")
def test_access_enable_disable_option(browser,wait10):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "a[href='/']").click()
    browser.find_element(By.CSS_SELECTOR, "button.jenkins-menu-dropdown-chevron").click()

    configure_locator = (By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']")
    wait10.until(EC.element_to_be_clickable(configure_locator)).click()

    enable_disable_locator = (By.ID, "enable-disable-project")
    wait10.until(EC.visibility_of_element_located(enable_disable_locator))

    assert f"/job/{project_name}/configure" in browser.current_url
    assert project_name in browser.find_element(By.TAG_NAME, "body").text
    assert browser.find_element(*enable_disable_locator).is_displayed()
    assert browser.find_element(*enable_disable_locator).is_selected()

@pytest.mark.skip
@pytest.mark.dependency(name="project_disabled", depends=["project_created"])
def test_disable_freestyle_project(browser, wait10):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/']").click()

    project_locator = (By.CSS_SELECTOR, f"a[href='job/{project_name}/']")
    wait10.until(EC.element_to_be_clickable(project_locator)).click()

    configure_locator = (By.LINK_TEXT, "Configure")
    wait10.until(EC.element_to_be_clickable(configure_locator)).click()

    browser.find_element(By.CSS_SELECTOR, "label[for='enable-disable-project']").click()
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        "This project is currently disabled"
    ))

    assert "This project is currently disabled" in browser.find_element(By.TAG_NAME, "body").text

@pytest.mark.skip
@pytest.mark.dependency(name="disabled_state_saved", depends=["project_disabled"])
def test_save_freestyle_project_disabled_state(browser, wait5):
    project_name = "Freestyle_Project_Config_Test"

    project_locator = (By.LINK_TEXT, project_name)
    wait5.until(EC.element_to_be_clickable(project_locator)).click()

    wait5.until(EC.url_contains(f"/job/{project_name}/"))

    browser.refresh()

    wait5.until(EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        "This project is currently disabled"
    ))

    assert "This project is currently disabled" in browser.find_element(By.TAG_NAME, "body").text
    assert browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']" ).is_displayed()

@pytest.mark.skip
@pytest.mark.dependency(depends=["disabled_state_saved"])
def test_enable_disabled_freestyle_project(browser, wait10):
    project_name = "Freestyle_Project_Config_Test"

    project_locator = (By.LINK_TEXT, project_name)
    wait10.until(EC.element_to_be_clickable(project_locator)).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element( By.CSS_SELECTOR,"button[name='Submit'][value='Enable']").click()

    wait10.until(EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        project_name
    ))

    assert "This project is currently disabled" not in browser.find_element(By.TAG_NAME, "body").text
    assert len(browser.find_elements(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")) == 0

def test_environment_options_are_available(browser, wait10):
    project_name = "Freestyle_Environment_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

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


def test_create_project_without_environment_settings(browser, wait10):
    project_name = "Freestyle_Environment_Default_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

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


def test_create_freestyle_project_and_check_scm_types(browser, wait10):
    project_name = "Freestyle_SCM_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])" ).click()

    freestyle_selected = browser.find_element(By.CSS_SELECTOR, "input[value='hudson.model.FreeStyleProject']" ).is_selected()

    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    assert freestyle_selected
    assert browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Source Code Management']]").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-0']").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").is_displayed()
    assert browser.find_element(By.ID, "radio-block-0").is_selected()


def test_git_scm_fields_are_displayed_when_git_is_selected(browser, wait10):
    project_name = "Freestyle_Git_SCM_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element( By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])" ).click()

    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.XPATH,"//button[.//span[normalize-space()='Source Code Management']]" ).click()

    browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url = wait10.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='_.url']"))
    )

    credentials = browser.find_element( By.CSS_SELECTOR, "select[name='_.credentialsId']")

    branch = wait10.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='_.name'][default='*/master']"))
    )

    assert repository_url.is_displayed()
    assert credentials.is_displayed()
    assert branch.is_displayed()


def test_error_message_for_invalid_git_repository_url(browser, wait10):
    project_name = "Freestyle_Invalid_Git_URL_Test"
    invalid_repository_url = "https://github.com/invalid-user/non-existing-repository.git"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR,"label:has(input[value='hudson.model.FreeStyleProject'])").click()

    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element( By.XPATH,"//button[.//span[normalize-space()='Source Code Management']]").click()

    browser.find_element( By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url_field = wait10.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='_.url']")
        )
    )
    repository_url_field.send_keys(invalid_repository_url)

    repository_url_field.send_keys(Keys.TAB)

    wait10.until(
        EC.text_to_be_present_in_element((
            By.XPATH,
            "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"
        ), "Failed to connect to repository")
    )

    error_message = browser.find_element(
        By.XPATH,
        "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"
    )

    assert "Failed to connect to repository" in error_message.text