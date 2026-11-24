from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

from pages.home_page import HomePage
from pages.manage_jenkins_page import ManageJenkinsPage

JOB_NAME = "Job_1"

def test_welcome_message_and_start_page(browser):
    home_page = HomePage(browser)

    assert home_page.get_welcome_title() == "Welcome to Jenkins!"
    assert home_page.is_create_job_displayed()
    assert home_page.is_setup_agent_displayed()
    assert home_page.is_configure_cloud_displayed()
    assert home_page.is_learn_more_displayed()
    assert home_page.is_add_description_displayed()
    assert home_page.is_new_item_displayed()

def test_new_job_via_create_job_link(browser):
    new_job = (
        HomePage(browser)
        .click_create_job()
        .set_item_name(JOB_NAME)
        .select_pipeline_and_click_ok()
        .goto_home_page()
        .get_first_project_name()
    )

    assert new_job == JOB_NAME

def test_manage_jenkins(browser):

    HomePage(browser).click_manage_jenkins()

    expected_groups = ['System Configuration',
                       'Security',
                       'Status Information',
                       'Troubleshooting',
                       'Tools and Actions']

    expected_options = ['System', 'Tools', 'Plugins', 'Nodes', 'Clouds', 'Appearance',
                        'Security', 'Credentials', 'Credential Providers', 'Users',
                        'System Information', 'Logs', 'Load Statistics', 'About Jenkins',
                        'Manage Old Data',
                        'Reload Configuration from Disk', 'Jenkins CLI', 'Script Console', 'Prepare for Shutdown']

    groups = ManageJenkinsPage(browser).get_group_names()
    options = ManageJenkinsPage(browser).get_option_names()

    assert groups == expected_groups
    assert options == expected_options

@pytest.mark.skip(reason="failed")
def test_expand_build_queue(browser):
    home_page = HomePage(browser)

    if home_page.is_build_queue_expanded():
        home_page.toggle_build_queue()

    home_page.toggle_build_queue()

    assert home_page.is_build_queue_expanded()
    assert home_page.is_build_queue_content_displayed()

def test_collapse_build_queue(browser):
    home_page = HomePage(browser)

    if not home_page.is_build_queue_expanded():
        home_page.toggle_build_queue()

    home_page.toggle_build_queue()

    assert not home_page.is_build_queue_expanded()
    assert not home_page.is_build_queue_content_displayed()
