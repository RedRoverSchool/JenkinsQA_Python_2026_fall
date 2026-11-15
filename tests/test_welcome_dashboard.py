
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

JOB_NAME = "Job_1"

def test_welcome_message_and_start_page(browser, wait5):

    welcome_title = browser.find_element(By.XPATH, "//div[@class='empty-state-block']/h1")
    create_job = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='newJob']"))
    )
    setup_agent = browser.find_element(By.XPATH, "//a[@href='computer/new']")
    configure_cloud = browser.find_element(By.XPATH, "//a[@href='cloud/']")
    learn_more = browser.find_element(By.XPATH, "//a[contains(@href,'jenkins.io')]")
    description = browser.find_element(By.ID, "description-link")
    new_item = browser.find_element(By.XPATH, "//a[@href='/view/all/newJob']")

    assert welcome_title.text == "Welcome to Jenkins!"
    assert create_job.is_displayed()
    assert setup_agent.is_displayed()
    assert configure_cloud.is_displayed()
    assert learn_more.is_displayed()
    assert description.is_displayed()
    assert new_item.is_displayed()

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
