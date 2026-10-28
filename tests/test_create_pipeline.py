from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_create_pipeline(browser):
    new_item = browser.find_element(By.CSS_SELECTOR, "#tasks > div:nth-child(1) > span > a")
    new_item.click()
    name_input = browser.find_element(By.ID, "name")
    name_input.send_keys("new-pipeline")
    pipeline = browser.find_element(By.CSS_SELECTOR, "[class*='job_WorkflowJob']")
    pipeline.click()
    create_ok = browser.find_element(By.ID, "ok-button")
    create_ok.click()

    WebDriverWait(browser, 10).until(EC.url_contains("/job/new-pipeline/configure"))