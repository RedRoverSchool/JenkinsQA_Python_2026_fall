import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.pipeline_configuration_page import PipelineConfigurationPage
from pages.home_page import HomePage

@pytest.mark.dependency()
def test_create_pipeline(browser, wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "#tasks > div:nth-child(1) > span > a")
    new_item.click()
    name_input = browser.find_element(By.ID, "name")
    name_input.send_keys("new-pipeline")
    pipeline = browser.find_element(By.CSS_SELECTOR, "[class*='job_WorkflowJob']")
    pipeline.click()
    create_ok = browser.find_element(By.ID, "ok-button")
    create_ok.click()
    triggers = wait10.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'jenkins-section__title') and contains(., 'Triggers')]")))

    assert triggers.text == "Triggers"


@pytest.mark.dependency(depends=["test_create_pipeline"])
def test_edit_pipeline(browser, wait10):
    pipeline_link = browser.find_element(By.CSS_SELECTOR, "a[href='job/new-pipeline/']")
    ActionChains(browser).move_to_element(pipeline_link).perform()

    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='job/new-pipeline/'] .jenkins-menu-dropdown-chevron"))).click()

    wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".jenkins-dropdown")))
    wait10.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.jenkins-dropdown__item[href='/job/new-pipeline/configure']"))).click()

    wait10.until(EC.url_contains("/job/new-pipeline/configure"))
    triggers = wait10.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'jenkins-section__title') and contains(., 'Triggers')]")))

    assert "/job/new-pipeline/configure" in browser.current_url
    assert triggers.text == "Triggers"


@pytest.mark.dependency(depends=["test_create_pipeline"])
def test_triggers_display_checkboxes_and_help_icons(browser):
    config_page = (
        HomePage(browser)
        .click_pipeline("new-pipeline")
        .open_configuration_pipeline_page()
        .click_on_left_side_section(PipelineConfigurationPage.ClickOnLeftSideSection.TRIGGERS)
    )
    assert config_page.are_triggers_checkboxes_and_help_icons_displayed()