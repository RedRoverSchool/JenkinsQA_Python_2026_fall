from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_multibranch_pipeline(browser):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys("FirstPipeline")
    browser.find_element(By.XPATH, "//span[normalize-space()='Multibranch Pipeline']").click()
    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.NAME, "_.displayNameOrNull"))
    )

    browser.find_element(By.NAME, "_.displayNameOrNull").send_keys("PipelineDisplayName")
    browser.find_element(By.NAME, "_.description").send_keys("PipelineDescriptions")
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "PipelineDisplayName")
    )

    assert "PipelineDisplayName" in browser.find_element(By.TAG_NAME, "h1").text

def test_create_multibranch_pipeline(browser):
    """TC_01.005.01 | Verify successful creation of a Multibranch Pipeline"""

    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    pipeline = browser.find_element(By.XPATH, "//*[contains(@class, 'multibranch')]")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jenkins-breadcrumbs__list"))
    )
    breadcrumbs_text = browser.find_element(By.CLASS_NAME, "jenkins-breadcrumbs__list").text

    assert pipeline_name in breadcrumbs_text
    assert f"job/{pipeline_name}/configure" in browser.current_url
