from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_open_new_item_page(browser):
    new_item_link = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item_link.click()
    assert "/view/all/newJob" in browser.current_url

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "name")))

    items_type_list = browser.find_element(By.ID, "items")
    assert items_type_list.is_displayed()

    pipeline_item = browser.find_element(By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    pipeline_label = pipeline_item.find_element(By.CLASS_NAME, "jenkins-choice-list__item__label")
    assert pipeline_item.is_displayed() and pipeline_label.text == "Pipeline"