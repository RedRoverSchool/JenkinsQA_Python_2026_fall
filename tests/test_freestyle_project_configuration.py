import pytest
from selenium.webdriver.common.by import By
from pages.home_page import HomePage

PROJECT_NAME = "Freestyle_Project_Config_Test"
SAVE_DESCRIPTION = "Test project configuration saved successfully"
APPLY_DESCRIPTION = "Test project configuration applied successfully"
EXPECTED_POST_BUILD_ACTIONS = [
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

@pytest.mark.dependency(name="project_created")
def test_create_project_and_access_enable_disable_option(browser):
    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PROJECT_NAME)
        .select_freestyle_and_click_ok()
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
    )

    assert f"/job/{PROJECT_NAME}/configure" in browser.current_url
    assert PROJECT_NAME in browser.find_element(By.TAG_NAME, "body").text
    assert configuration_page.is_enable_disable_displayed()
    assert configuration_page.is_enable_disable_selected()


@pytest.mark.dependency(name="project_disabled", depends=["project_created"])
def test_disable_freestyle_project(browser):
    project_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .disable_project()
        .click_save()
    )

    assert project_page.is_project_disabled()


@pytest.mark.dependency(name="disabled_state_saved", depends=["project_disabled"])
def test_save_freestyle_project_disabled_state(browser):
    project_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .refresh_page()
    )

    assert project_page.is_project_disabled()
    assert project_page.is_enable_button_displayed()


@pytest.mark.dependency(depends=["disabled_state_saved"])
def test_enable_disabled_freestyle_project(browser):
    project_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .enable_project()
    )

    assert project_page.is_project_enabled()
    assert project_page.is_enable_button_hidden()


@pytest.mark.dependency(
    name="environment_options_available",
    depends=["project_created"]
)
def test_environment_options_are_available(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_environment()
    )

    assert configuration_page.are_environment_options_displayed()


@pytest.mark.dependency(depends=["environment_options_available"])
def test_create_project_without_environment_settings(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_environment()
    )

    assert configuration_page.are_environment_options_unselected()


@pytest.mark.dependency(
    name="scm_types_checked",
    depends=["project_created"]
)
def test_scm_types_are_displayed(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_scm()
    )

    assert configuration_page.are_scm_options_displayed()
    assert configuration_page.is_none_scm_selected()


@pytest.mark.dependency(
    name="git_fields_checked",
    depends=["scm_types_checked"]
)
def test_git_scm_fields_are_displayed_when_git_is_selected(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_scm()
        .select_git_scm()
    )

    assert configuration_page.are_git_fields_displayed()

@pytest.mark.dependency(
    name="invalid_git_url_checked",
    depends=["git_fields_checked"]
)
def test_error_message_for_invalid_git_repository_url(browser):
    invalid_repository_url = "https://github.com/invalid-user/non-existing-repository.git"

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_scm()
        .select_git_scm()
        .enter_repository_url(invalid_repository_url)
    )

    assert configuration_page.is_git_error_displayed()


@pytest.mark.dependency(
    name="build_triggers_project_created",
    depends=["project_created"]
)
def test_build_triggers_options_are_available(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    triggers_available = configuration_page.are_build_trigger_options_available()
    configuration_page.click_save()

    assert triggers_available


@pytest.mark.dependency(
    name="build_triggers_default_checked",
    depends=["build_triggers_project_created"]
)
def test_build_triggers_are_disabled_by_default(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    triggers_unselected = configuration_page.are_build_trigger_options_unselected()
    configuration_page.click_save()

    assert triggers_unselected


@pytest.mark.dependency(
    name="remote_build_trigger_configured",
    depends=["build_triggers_default_checked"]
)
def test_configure_remote_build_trigger_with_authentication_token(browser):
    token = "RemoteBuildToken123"

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
        .enable_remote_build_trigger()
        .enter_authentication_token(token)
    )

    configuration_page.click_save()

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    remote_trigger_selected = configuration_page.is_remote_build_trigger_selected()

    assert remote_trigger_selected


@pytest.mark.dependency(
    name="build_periodically_configured",
    depends=["remote_build_trigger_configured"]
)
def test_configure_build_periodically_with_valid_schedule(browser):
    schedule = "H/5 * * * *"

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
        .enable_build_periodically()
        .enter_build_periodically_schedule(schedule)
    )

    configuration_page.click_save()

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    build_periodically_selected = configuration_page.is_build_periodically_selected()
    saved_schedule = configuration_page.get_build_periodically_schedule()

    assert build_periodically_selected
    assert saved_schedule == schedule


@pytest.mark.dependency(
    name="poll_scm_configured",
    depends=["build_periodically_configured"]
)
def test_configure_poll_scm_with_valid_schedule(browser):
    schedule = "H/5 * * * *"

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
        .enable_poll_scm()
        .enter_poll_scm_schedule(schedule)
    )

    configuration_page.click_save()

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    poll_scm_selected = configuration_page.is_poll_scm_selected()
    saved_schedule = configuration_page.get_poll_scm_schedule()

    assert poll_scm_selected
    assert saved_schedule == schedule

@pytest.mark.dependency(
    name="build_after_other_projects_configured",
    depends=["poll_scm_configured"]
)
def test_configure_build_after_other_projects_are_built(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
        .enable_build_after_projects()
    )

    configuration_page.click_save()

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    build_after_projects_selected = (
        configuration_page.is_build_after_projects_selected()
    )
    projects_to_watch_available = (
        configuration_page.are_projects_to_watch_available()
    )
    success_threshold_selected = (
        configuration_page.is_success_threshold_selected()
    )
    other_thresholds_displayed = (
        configuration_page.are_other_thresholds_displayed()
    )

    assert build_after_projects_selected
    assert projects_to_watch_available
    assert success_threshold_selected
    assert other_thresholds_displayed


@pytest.mark.dependency(
    name="build_triggers_helper_tooltips_checked",
    depends=["build_after_other_projects_configured"]
)
def test_build_triggers_helper_tooltips(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_build_triggers()
    )

    tooltips_correct = (
        configuration_page.are_build_trigger_helper_tooltips_correct()
    )

    assert tooltips_correct


@pytest.mark.dependency(
    name="post_build_actions_available",
    depends=["project_created"]
)
def test_post_build_actions_options_are_available(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_post_build_actions()
        .click_add_post_build_action()
    )

    available_actions = configuration_page.get_available_post_build_actions()

    configuration_page.click_save()

    assert all(action in available_actions for action in EXPECTED_POST_BUILD_ACTIONS)


@pytest.mark.dependency(
    depends=["post_build_actions_available"]
)
def test_multiple_post_build_actions_can_be_added(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .click_post_build_actions()
        .add_post_build_actions(
            ["Archive the artifacts", "E-mail Notification"]
        )
    )

    configuration_page.click_save()

    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
    )
    assert "Archive the artifacts" in configuration_page.driver.page_source
    assert "E-mail Notification" in configuration_page.driver.page_source


@pytest.mark.dependency(
    name="save_apply_buttons_available",
    depends=["project_created"]
)
def test_save_apply_buttons_are_available(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
    )

    assert configuration_page.are_save_apply_buttons_available()


@pytest.mark.dependency(
    name="project_configuration_saved",
    depends=["project_created"]
)
def test_save_project_configuration(browser):
    project_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .enter_description(SAVE_DESCRIPTION)
        .click_save()
    )

    saved_description = project_page.get_description()

    assert PROJECT_NAME in browser.current_url
    assert saved_description == SAVE_DESCRIPTION


@pytest.mark.dependency(
    name="project_configuration_applied",
    depends=["project_created"]
)
def test_apply_project_configuration(browser):
    configuration_page = (
        HomePage(browser)
        .goto_home_page()
        .click_project(PROJECT_NAME)
        .click_configuration()
        .enter_description(APPLY_DESCRIPTION)
        .click_apply()
    )

    saved_description = configuration_page.get_description()

    assert f"/job/{PROJECT_NAME}/configure" in browser.current_url
    assert saved_description == APPLY_DESCRIPTION

