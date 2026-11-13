from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_add_description_to_multiconfiguration_project(browser, wait5):

    project_description = "This is my multi-configuration project"

    browser.find_element(By.CSS_SELECTOR, ".task-link.task-link-no-confirm ").click()
    project_name = browser.find_element(By.XPATH, "//*[@id='name']")
    project_name.click()
    project_name.send_keys("my multi-configuration project")
    browser.find_element(By.XPATH, "//span[text()='Multi-configuration project']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(EC.visibility_of_element_located((By.NAME, "description")))

    project_description = browser.find_element(By.NAME, "description")
    project_description.click()
    project_description.send_keys("This is my multi-configuration project")
    browser.find_element(By.CSS_SELECTOR, ".jenkins-button.jenkins-submit-button.jenkins-button--primary").click()

    assert project_description.text in browser.find_element(By.TAG_NAME, "h1").text


