import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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
    menu_dropdown = pipeline_link.find_element(By.CSS_SELECTOR, ".jenkins-menu-dropdown-chevron")
    menu_dropdown.click()
    configure_button = wait10.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@class, 'jenkins-dropdown__item') and contains(., 'Configure')]")))
    configure_button.click()
    triggers = wait10.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'jenkins-section__title') and contains(., 'Triggers')]")))

    assert triggers.text == "Triggers"
