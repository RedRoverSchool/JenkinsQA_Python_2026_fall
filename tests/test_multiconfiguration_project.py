import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.dependency()
def test_add_description_to_multiconfiguration_project(browser, wait2):

    project_description = "This is my multi-configuration project"

    browser.find_element(By.CSS_SELECTOR, ".task-link.task-link-no-confirm ").click()
    project_name = browser.find_element(By.XPATH, "//*[@id='name']")
    project_name.click()
    project_name.send_keys("my multi-configuration project")
    multi_configuration_radio_button = browser.find_element(By.XPATH, "//label[contains(., 'Multi-configuration project')]")
    multi_configuration_radio_button.click()

    wait2.until(EC.element_to_be_clickable((By.ID, "ok-button"))).click()

    wait2.until(EC.visibility_of_element_located((By.NAME, "description")))

    description_field = browser.find_element(By.NAME, "description")
    description_field.click()
    description_field.send_keys(project_description)
    browser.find_element(By.CSS_SELECTOR, ".jenkins-button.jenkins-submit-button.jenkins-button--primary").click()

    wait2.until(EC.visibility_of_element_located((By.ID, "description-content")))

    assert project_description in browser.find_element(By.ID, "description-content").text


@pytest.mark.dependency(depends=["test_add_description_to_multiconfiguration_project"])
def test_verify_discard_old_builds_configuration_options(browser):

    browser.find_element(By.LINK_TEXT, "my multi-configuration project").click()
    browser.find_element(By.XPATH, "//a[contains(@href,'/configure')]").click()
    discard_old_builds_checkbox = browser.find_element(By.CLASS_NAME, "jenkins-checkbox")
    discard_old_builds_checkbox.click()
    days_to_keep_field = browser.find_element(By.NAME, "_.daysToKeepStr")
    days_to_keep_field.send_keys("7")
    builds_to_keep_field = browser.find_element(By.NAME, "_.numToKeepStr")
    builds_to_keep_field.send_keys("20")
    browser.find_element(By.CSS_SELECTOR, ".jenkins-button.jenkins-submit-button.jenkins-button--primary").click()

    browser.find_element(By.XPATH, "//a[contains(@href,'/configure')]").click()

    assert browser.find_element(By.NAME, "_.daysToKeepStr").get_attribute("value") == "7"
    assert browser.find_element(By.NAME, "_.numToKeepStr").get_attribute("value") == "20"
    assert browser.find_element(By.ID, "cb2").is_selected()


