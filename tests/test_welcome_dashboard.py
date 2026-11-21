import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

def test_create_job(browser, wait5):

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='newJob']"))
    ).click()

    browser.find_element(By.ID, "name").send_keys(JOB_NAME)
    wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'WorkflowJob')]"))
    ).click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[@class='app-jenkins-logo']").click()

    job = browser.find_element(By.XPATH, f"//a[@href='job/{JOB_NAME}/' and contains(@class,'jenkins-table__link')]")
    assert job.is_displayed()

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

def test_build_queue(browser, wait5):

    expand_collapse_locator = (By.XPATH, "//a[contains(@href,'buildQueue')]")
    queue_message_locator = (By.XPATH, "//td[text()='No builds in the queue.']")
    welcome_title_locator = (By.XPATH, "//div[@class='empty-state-block']/h1")

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='buildQueue']"))
    )

    expand_collapse = browser.find_element(*expand_collapse_locator)
    if expand_collapse.get_attribute("title") == "collapse":
        expand_collapse.click()
        wait5.until(
            EC.text_to_be_present_in_element_attribute(expand_collapse_locator, "title", "expand")
        )

    browser.find_element(*expand_collapse_locator).click()
    queue_message = wait5.until(
        EC.visibility_of_element_located(queue_message_locator)
    )

    browser.find_element(*expand_collapse_locator).click()
    is_hidden = wait5.until(
        EC.invisibility_of_element_located(queue_message)
    )
    assert is_hidden
    assert browser.find_element(*welcome_title_locator).is_displayed()
