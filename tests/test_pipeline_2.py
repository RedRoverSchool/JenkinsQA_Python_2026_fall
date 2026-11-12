from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_create_pipeline(browser, wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "#tasks > div:nth-child(1) > span > a")
    new_item.click()
    name_input = browser.find_element(By.ID, "name")
    name_input.send_keys("new-pipeline")
    pipeline = browser.find_element(By.CSS_SELECTOR, "[class*='job_WorkflowJob']")
    pipeline.click()
    create_ok = browser.find_element(By.ID, "ok-button")
    create_ok.click()
    triggers = wait10.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'jenkins-section__title') and contains(., 'Triggers')]")))

    assert triggers.text == "Triggers"