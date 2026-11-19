import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.dependency(name="project_created")
def test_access_enable_disable_option(browser, wait10):
    project_name = "Freestyle_Project_Config_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(By.XPATH,"//span[normalize-space()='Freestyle project']/parent::label").click()
    browser.find_element(By.ID, "ok-button").submit()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "a[href='/']").click()

    dropdown_locator = ( By.CSS_SELECTOR,"button.jenkins-menu-dropdown-chevron")
    wait10.until(EC.element_to_be_clickable(dropdown_locator)).click()

    configure_locator = ( By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']" )
    wait10.until(EC.visibility_of_element_located(configure_locator))
    browser.find_element(*configure_locator).click()

    enable_disable_locator = (By.ID, "enable-disable-project")
    wait10.until(EC.visibility_of_element_located(enable_disable_locator))

    assert f"/job/{project_name}/configure" in browser.current_url
    assert project_name in browser.find_element(By.TAG_NAME, "body").text
    assert browser.find_element(*enable_disable_locator).is_displayed()
    assert browser.find_element(*enable_disable_locator).is_selected()


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


@pytest.mark.dependency(depends=["disabled_state_saved"])
def test_enable_disabled_freestyle_project(browser, wait10):
    project_name = "Freestyle_Project_Config_Test"

    project_locator = (By.LINK_TEXT, project_name)
    wait10.until(EC.element_to_be_clickable(project_locator)).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element( By.CSS_SELECTOR,"button[name='Submit'][value='Enable']").click()

    wait10.until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[contains(text(), 'This project is currently disabled')]")
    ))

    assert "This project is currently disabled" not in browser.find_element(By.TAG_NAME, "body").text
    assert len(browser.find_elements(By.CSS_SELECTOR, "button[name='Submit'][value='Enable']")) == 0


@pytest.mark.dependency(name="environment_project_created")
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


@pytest.mark.dependency(depends=["environment_project_created"])
def test_create_project_without_environment_settings(browser, wait10):
    browser.find_element( By.CSS_SELECTOR,"a[href='job/Freestyle_Environment_Test/']").click()

    wait10.until(EC.url_contains("/job/Freestyle_Environment_Test/"))

    browser.find_element( By.CSS_SELECTOR, "a[href='/job/Freestyle_Environment_Test/configure']").click()

    wait10.until(EC.url_contains("/configure"))

    browser.find_element( By.XPATH, "//button[.//span[normalize-space()='Environment']]" ).click()

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


@pytest.mark.dependency(name="scm_project_created")
def test_create_freestyle_project_and_check_scm_types(browser, wait10):
    project_name = "Freestyle_SCM_Test"

    browser.find_element( By.CSS_SELECTOR, "a[href='/view/all/newJob']" ).click()

    name_field = browser.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])" ).click()

    freestyle_selected = browser.find_element(By.CSS_SELECTOR, "input[value='hudson.model.FreeStyleProject']" ).is_selected()

    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains("/job/"))

    assert freestyle_selected
    assert browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Source Code Management']]").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-0']").is_displayed()
    assert browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").is_displayed()
    assert browser.find_element(By.ID, "radio-block-0").is_selected()


@pytest.mark.dependency(name="git_fields_checked", depends=["scm_project_created"])
def test_git_scm_fields_are_displayed_when_git_is_selected(browser, wait10):
    project_name = "Freestyle_SCM_Test"

    browser.find_element(By.CSS_SELECTOR, f"a[href='job/{project_name}/']").click()
    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "a[href='/job/Freestyle_SCM_Test/configure']").click()
    browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='_.url']")))
    credentials = browser.find_element(By.CSS_SELECTOR, "select[name='_.credentialsId']")
    branch = wait10.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='_.name'][default='*/master']")))

    assert repository_url.is_displayed()
    assert credentials.is_displayed()
    assert branch.is_displayed()


@pytest.mark.dependency(name="invalid_git_url_checked", depends=["git_fields_checked"])
def test_error_message_for_invalid_git_repository_url(browser, wait10):
    project_name = "Freestyle_SCM_Test"
    invalid_repository_url = "https://github.com/invalid-user/non-existing-repository.git"

    browser.find_element(By.CSS_SELECTOR, f"a[href='job/{project_name}/']").click()
    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "a[href='/job/Freestyle_SCM_Test/configure']").click()
    browser.find_element(By.XPATH, "//button[.//span[normalize-space()='Source Code Management']]").click()
    browser.find_element(By.CSS_SELECTOR, "label[for='radio-block-1']").click()

    repository_url_field = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='_.url']")))
    repository_url_field.send_keys(invalid_repository_url)
    repository_url_field.send_keys(Keys.TAB)

    wait10.until(EC.text_to_be_present_in_element(
        (By.XPATH, "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"),
        "Failed to connect to repository"))

    error_message = browser.find_element(By.XPATH,
                                         "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]")

    assert "Failed to connect to repository" in error_message.text


@pytest.mark.dependency(name="build_triggers_project_created")
def test_build_triggers_options_are_available(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()

    name_field = browser.find_element(By.ID, "name")
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()
    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    triggers_section = browser.find_element(By.ID, "54-72-69-67-67-65-72-73")
    triggers_section.click()

    remote_trigger = browser.find_element(By.ID, "cb13")
    build_after_other_projects = browser.find_element(By.ID, "cb14")
    build_periodically = browser.find_element(By.ID, "cb15")
    github_hook_trigger = browser.find_element(By.ID, "cb16")
    poll_scm = browser.find_element(By.ID, "cb17")

    triggers_displayed = triggers_section.is_displayed()
    remote_displayed = remote_trigger.is_displayed() and remote_trigger.is_enabled()
    build_after_displayed = build_after_other_projects.is_displayed() and build_after_other_projects.is_enabled()
    periodic_displayed = build_periodically.is_displayed() and build_periodically.is_enabled()
    github_displayed = github_hook_trigger.is_displayed() and github_hook_trigger.is_enabled()
    poll_scm_displayed = poll_scm.is_displayed() and poll_scm.is_enabled()

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    assert triggers_displayed
    assert remote_displayed
    assert build_after_displayed
    assert periodic_displayed
    assert github_displayed
    assert poll_scm_displayed


@pytest.mark.dependency(name="build_triggers_default_checked",depends=["build_triggers_project_created"])
def test_build_triggers_are_disabled_by_default(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"

    project_link = (By.CSS_SELECTOR, f"a[href='job/{project_name}/']")
    wait10.until(EC.element_to_be_clickable(project_link)).click()

    configure_link = (By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']")
    wait10.until(EC.element_to_be_clickable(configure_link)).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    remote_trigger = browser.find_element(By.ID, "cb13").is_selected()
    build_after_other_projects = browser.find_element(By.ID, "cb14").is_selected()
    build_periodically = browser.find_element(By.ID, "cb15").is_selected()
    github_hook_trigger = browser.find_element(By.ID, "cb16").is_selected()
    poll_scm = browser.find_element(By.ID, "cb17").is_selected()

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    assert remote_trigger is False
    assert build_after_other_projects is False
    assert build_periodically is False
    assert github_hook_trigger is False
    assert poll_scm is False


@pytest.mark.dependency(name="remote_build_trigger_configured",depends=["build_triggers_default_checked"])
def test_configure_remote_build_trigger_with_authentication_token(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"

    wait10.until(EC.element_to_be_clickable( (By.CSS_SELECTOR, f"a[href='job/{project_name}/']"))).click()

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']"))).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    remote_trigger_label = browser.find_element(By.XPATH, "//label[contains(., 'Trigger builds remotely')]")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", remote_trigger_label)
    remote_trigger_label.click()

    browser.find_element(By.NAME, "authToken").send_keys("RemoteBuildToken123")
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))
    browser.find_element(By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']" ).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    remote_trigger_enabled = browser.find_element(By.ID, "cb13").is_selected()

    assert remote_trigger_enabled


@pytest.mark.dependency(name="build_periodically_configured", depends=["remote_build_trigger_configured"])
def test_configure_build_periodically_with_valid_schedule(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"
    schedule = "H/5 * * * *"

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='job/{project_name}/']") )).click()

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']"))).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    periodic_trigger_label = browser.find_element(By.XPATH, "//label[contains(., 'Build periodically')]")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", periodic_trigger_label)
    periodic_trigger_label.click()

    browser.find_element(By.CSS_SELECTOR, "textarea[name='_.spec']").send_keys(schedule)
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))
    browser.find_element(By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    periodic_trigger = browser.find_element(By.CSS_SELECTOR, "input[name='hudson-triggers-TimerTrigger']").is_selected()
    saved_schedule = browser.find_element(By.CSS_SELECTOR, "textarea[name='_.spec']").get_attribute("value")

    assert periodic_trigger
    assert saved_schedule == schedule


@pytest.mark.dependency(name="poll_scm_configured", depends=["build_periodically_configured"])
def test_configure_poll_scm_with_valid_schedule(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"
    schedule = "H/5 * * * *"

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='job/{project_name}/']"))).click()

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']"))).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    poll_scm_label = browser.find_element(By.XPATH, "//label[contains(., 'Poll SCM')]")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", poll_scm_label)
    poll_scm_label.click()

    poll_scm_schedule = browser.find_element( By.XPATH, "//label[contains(., 'Poll SCM')]/following::textarea[1]" )
    poll_scm_schedule.send_keys(schedule)

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    poll_scm_enabled = browser.find_element(By.ID, "cb17").is_selected()

    saved_schedule = browser.find_element(By.XPATH, "//label[contains(., 'Poll SCM')]/following::textarea[1]").get_attribute("value")

    assert poll_scm_enabled
    assert saved_schedule == schedule

@pytest.mark.dependency(name="build_after_other_projects_configured", depends=["poll_scm_configured"])
def test_configure_build_after_other_projects_are_built(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='job/{project_name}/']"))).click()

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']"))).click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    build_after_projects_checkbox = browser.find_element(By.ID, "cb14")

    if not build_after_projects_checkbox.is_selected():
        build_after_projects_label = browser.find_element(By.XPATH, "//label[contains(., 'Build after other projects are built')]")
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", build_after_projects_label)
        build_after_projects_label.click()

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))
    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    projects_to_watch = wait10.until(EC.visibility_of_element_located((By.NAME, "_.upstreamProjects")))

    success_radio = browser.find_element(By.CSS_SELECTOR, "input[name='ReverseBuildTrigger.threshold'][value='SUCCESS']")

    build_after_projects_enabled = browser.find_element(By.ID, "cb14").is_selected()
    projects_to_watch_displayed = projects_to_watch.is_displayed()
    projects_to_watch_enabled = projects_to_watch.is_enabled()

    success_selected = success_radio.is_selected()

    unstable_displayed = browser.find_element(By.XPATH, "//div[contains(@class, 'jenkins-radio')][.//input[@value='UNSTABLE']]/label").is_displayed()
    failure_displayed = browser.find_element(By.XPATH, "//div[contains(@class, 'jenkins-radio')][.//input[@value='FAILURE']]/label").is_displayed()
    aborted_displayed = browser.find_element(By.XPATH, "//div[contains(@class, 'jenkins-radio')][.//input[@value='ABORTED']]/label").is_displayed()

    assert build_after_projects_enabled
    assert projects_to_watch_displayed
    assert projects_to_watch_enabled
    assert success_selected
    assert unstable_displayed
    assert failure_displayed
    assert aborted_displayed


@pytest.mark.dependency(
    name="build_triggers_helper_tooltips_checked",
    depends=["build_after_other_projects_configured"]
)
def test_build_triggers_helper_tooltips(browser, wait10):
    project_name = "Freestyle_Build_Triggers_Options_Test"

    project_link = (By.CSS_SELECTOR, f"a[href='job/{project_name}/']")
    configure_link = (By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']")

    wait10.until(EC.element_to_be_clickable(project_link)).click()
    wait10.until(EC.element_to_be_clickable(configure_link)).click()
    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    browser.find_element(By.CSS_SELECTOR, "div.jenkins-section__title").click()

    jenkins_url = browser.current_url.split("/job/")[0]

    help_buttons = [
        ("Build periodically", "Provides a cron -like feature to periodically execute this project."),
        ("Poll SCM", "Configure Jenkins to poll changes in SCM."),
        ("Build after other projects are built",
         "Set up a trigger so that when some other projects finish building, a new build is scheduled for this project.")
    ]

    help_urls = []

    for name, expected_text in help_buttons:
        locator = (By.CSS_SELECTOR, f"a[aria-label='Help for feature: {name}']")
        button = wait10.until(EC.presence_of_element_located(locator))
        help_urls.append((button.get_attribute("helpurl"), expected_text))

    help_results = []

    for help_url, expected_text in help_urls:
        browser.get(jenkins_url + help_url)
        help_text = wait10.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ).text
        help_results.append(expected_text in help_text)

    assert len(help_results) == 3
    assert all(help_results)


@pytest.mark.dependency(name="post_build_project_created")
def test_post_build_actions_options_are_available(browser, wait10):
    project_name = "Freestyle_Post_Build_Actions_Test"
    expected_actions = [
        "Aggregate downstream test results",
        "Archive the artifacts",
        "Build other projects",
        "Publish JUnit test result report",
        "Record fingerprints of files to track usage",
        "Git Publisher",
        "E-mail Notification",
        "Editable Email Notification",
        "Set GitHub commit status (universal)",
        "Delete workspace when build is done"
    ]

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()
    browser.find_element(By.ID, "name").send_keys(project_name)
    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()
    browser.find_element(By.ID, "ok-button").click()
    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    browser.find_element(By.CSS_SELECTOR, "button[data-section-id='50-6f-73-74-2d-62-75-69-6c-64-20-41-63-74-69-6f-6e-73']").click()
    add_button = browser.find_element(By.CSS_SELECTOR, "button.hetero-list-add[suffix='publisher']")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.hetero-list-add[suffix='publisher']"))).click()

    action_items = wait10.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.jenkins-dropdown__item")))
    available_actions = [item.get_attribute("textContent").strip() for item in action_items]

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()
    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    assert all(action in available_actions for action in expected_actions)


@pytest.mark.dependency(depends=["post_build_project_created"])
def test_multiple_post_build_actions_can_be_added(browser, wait10):
    project_name = "Freestyle_Post_Build_Actions_Test"

    project_link = (By.CSS_SELECTOR, f"a[href='job/{project_name}/']")
    configure_link = (By.CSS_SELECTOR, f"a[href='/job/{project_name}/configure']")

    wait10.until(EC.element_to_be_clickable(project_link)).click()
    wait10.until(EC.element_to_be_clickable(configure_link)).click()
    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    browser.find_element(By.CSS_SELECTOR, "button[data-section-id='50-6f-73-74-2d-62-75-69-6c-64-20-41-63-74-69-6f-6e-73']").click()

    add_button = (By.CSS_SELECTOR, "button.hetero-list-add[suffix='publisher']")

    for action in ["Archive the artifacts", "E-mail Notification"]:
        add_element = browser.find_element(*add_button)
        browser.execute_script("arguments[0].scrollIntoView({block: 'start'});", add_element)
        browser.execute_script("window.scrollBy(0, 250);")

        wait10.until(EC.element_to_be_clickable(add_button)).click()

        action_locator = (By.XPATH, f"//button[contains(@class, 'jenkins-dropdown__item') and normalize-space()='{action}']")
        wait10.until(EC.element_to_be_clickable(action_locator)).click()

    browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']").click()
    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    wait10.until(EC.element_to_be_clickable(configure_link)).click()
    wait10.until(EC.url_contains(f"/job/{project_name}/configure"))

    assert "Archive the artifacts" in browser.page_source
    assert "E-mail Notification" in browser.page_source

@pytest.mark.dependency(name="save_apply_project_created")
def test_save_apply_buttons_are_available(browser, wait10):
    project_name = "Freestyle_Save_Apply_Test"

    browser.find_element(By.CSS_SELECTOR, "a[href='newJob']").click()

    name_field = browser.find_element(By.ID, "name")
    name_field.send_keys(project_name)

    browser.find_element(By.CSS_SELECTOR, "label:has(input[value='hudson.model.FreeStyleProject'])").click()
    browser.find_element(By.ID, "ok-button").click()

    wait10.until(EC.url_contains(f"/job/{project_name}/"))

    save_button = browser.find_element(By.CSS_SELECTOR, "button[name='Submit'][value='Save']")
    apply_button = browser.find_element(By.CSS_SELECTOR, "button[name='Apply']")

    save_displayed = save_button.is_displayed() and save_button.is_enabled()
    apply_displayed = apply_button.is_displayed() and apply_button.is_enabled()

    configuration_url = browser.current_url
    save_button.click()

    wait10.until(EC.url_changes(configuration_url))

    assert save_displayed
    assert apply_displayed

