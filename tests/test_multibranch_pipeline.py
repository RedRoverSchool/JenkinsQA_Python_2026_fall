import secrets

import pytest
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
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    breadcrumbs_text = browser.find_element(By.CLASS_NAME, "jenkins-breadcrumbs__list").text

    assert pipeline_name in breadcrumbs_text
    assert f"job/{pipeline_name}/configure" in browser.current_url


def test_return_to_the_dashboard_without_creating_multibranch_pipeline(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.CLASS_NAME, "app-jenkins-logo").click()

    welcome_title = browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")

    assert welcome_title.text == "Welcome to Jenkins!"


def test_multibranch_with_special_characters(browser):
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    pipeline_name = "Pipeline" + spec_char

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=5).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    WebDriverWait(browser, timeout=5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = f"‘{spec_char}’ is an unsafe character"
    WebDriverWait(browser, timeout=5).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )

    error_message = browser.find_element(By.CLASS_NAME, "error").text
    ok_button = browser.find_element(By.ID, "ok-button")

    assert not ok_button.is_enabled()
    assert error_message == expected_text


def test_rename_multibranch_pipeline_from_dropdown_menu(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    chevron_selector = f"//button[@class='jenkins-menu-dropdown-chevron' and contains(@data-href,{pipeline_name})]"
    browser.find_element(By.XPATH, chevron_selector).click()
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    new_pipeline_name = "Pipeline_2"
    input_field = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(new_pipeline_name)
    browser.find_element(By.XPATH, "//button[@name='Submit']").click()

    job_name = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )

    assert new_pipeline_name == job_name.text
    assert f"job/{new_pipeline_name}" in browser.current_url


def test_rename_multibranch_pipeline_from_project_menu(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{pipeline_name}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    new_pipeline_name = "Pipeline_2"
    input_field = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(new_pipeline_name)
    browser.find_element(By.XPATH, "//button[@name='Submit']").click()

    job_name = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )

    assert new_pipeline_name == job_name.text
    assert f"job/{new_pipeline_name}" in browser.current_url


def test_rename_multibranch_pipeline_with_same_name(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{pipeline_name}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(pipeline_name)
    browser.find_element(By.TAG_NAME, "body").click()

    WebDriverWait(browser, timeout=5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = "The new name is the same as the current name."
    WebDriverWait(browser, timeout=5).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "warning"), expected_text)
    )
    warning_message = browser.find_element(By.CLASS_NAME, "warning").text

    assert warning_message == expected_text


def test_rename_multibranch_pipeline_with_blank_name(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{pipeline_name}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    browser.find_element(By.TAG_NAME, "body").click()

    WebDriverWait(browser, timeout=5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = "No name is specified"
    WebDriverWait(browser, timeout=5).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )
    error_message = browser.find_element(By.CLASS_NAME, "error").text

    assert error_message == expected_text


def test_rename_multibranch_pipeline_with_unsupported_characters(browser):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{pipeline_name}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()

    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    input_field.send_keys("Pipeline" + spec_char)
    browser.find_element(By.TAG_NAME, "body").click()

    WebDriverWait(browser, timeout=5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = f"‘{spec_char}’ is an unsafe character"
    WebDriverWait(browser, timeout=5).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )
    error_message = browser.find_element(By.CLASS_NAME, "error").text

    assert error_message == expected_text