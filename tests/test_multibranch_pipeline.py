import secrets
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

PIPELINE_NAME = "Pipeline_1"


def test_multibranch_pipeline(browser, wait5):
    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys("FirstPipeline")
    browser.find_element(By.XPATH, "//span[normalize-space()='Multibranch Pipeline']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.NAME, "_.displayNameOrNull"))
    )

    browser.find_element(By.NAME, "_.displayNameOrNull").send_keys("PipelineDisplayName")
    browser.find_element(By.NAME, "_.description").send_keys("PipelineDescriptions")
    browser.find_element(By.NAME, "Submit").click()

    wait5.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "PipelineDisplayName")
    )

    assert "PipelineDisplayName" in browser.find_element(By.TAG_NAME, "h1").text


def create_multibranch_pipeline(browser, wait5):
    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(PIPELINE_NAME)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = wait5.until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.NAME, "Submit").click()


@pytest.mark.dependency()
def test_create_multibranch_pipeline(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    pipeline_name = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )

    assert PIPELINE_NAME == pipeline_name.text
    assert f"job/{PIPELINE_NAME}/" in browser.current_url


def test_return_to_the_dashboard_without_creating_multibranch_pipeline(browser, wait5):
    pipeline_name = "Pipeline_1"

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = wait5.until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    browser.find_element(By.CLASS_NAME, "app-jenkins-logo").click()

    welcome_title = browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")

    assert welcome_title.text == "Welcome to Jenkins!"


def test_multibranch_with_special_characters(browser, wait5):
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    pipeline_name = "Pipeline" + spec_char

    browser.find_element(By.CSS_SELECTOR, ".task:nth-child(1)").click()
    browser.find_element(By.ID, "name").send_keys(pipeline_name)

    multibranch_locator = (By.XPATH, "//*[contains(@class, 'multibranch')]")
    pipeline = wait5.until(
        EC.element_to_be_clickable(multibranch_locator)
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pipeline)
    pipeline.click()

    wait5.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = f"‘{spec_char}’ is an unsafe character"
    wait5.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )

    error_message = browser.find_element(By.CLASS_NAME, "error").text
    ok_button = browser.find_element(By.ID, "ok-button")

    assert not ok_button.is_enabled()
    assert error_message == expected_text


@pytest.mark.dependency(depends=["test_create_multibranch_pipeline"])
def test_rename_multibranch_pipeline_from_dropdown_menu(browser, wait5, wait10):
    chevron_selector = f"//button[@class='jenkins-menu-dropdown-chevron' and contains(@data-href,{PIPELINE_NAME})]"
    browser.find_element(By.XPATH, chevron_selector).click()
    wait10.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'confirm-rename')]"))
    ).click()

    new_pipeline_name = "Pipeline_2"
    input_field = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(new_pipeline_name)
    browser.find_element(By.XPATH, "//button[@name='Submit']").click()

    job_name = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )

    assert new_pipeline_name == job_name.text
    assert f"job/{new_pipeline_name}" in browser.current_url


def test_rename_multibranch_pipeline_from_project_menu(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    new_pipeline_name = "Pipeline_2"
    input_field = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(new_pipeline_name)
    browser.find_element(By.XPATH, "//button[@name='Submit']").click()

    job_name = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )

    assert new_pipeline_name == job_name.text
    assert f"job/{new_pipeline_name}" in browser.current_url


def test_rename_multibranch_pipeline_with_same_name(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    input_field.send_keys(PIPELINE_NAME)
    browser.find_element(By.TAG_NAME, "body").click()

    wait5.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = "The new name is the same as the current name."
    wait5.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "warning"), expected_text)
    )
    warning_message = browser.find_element(By.CLASS_NAME, "warning").text

    assert warning_message == expected_text


def test_rename_multibranch_pipeline_with_blank_name(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()
    browser.find_element(By.TAG_NAME, "body").click()

    wait5.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = "No name is specified"
    wait5.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )
    error_message = browser.find_element(By.CLASS_NAME, "error").text

    assert error_message == expected_text


def test_rename_multibranch_pipeline_with_unsupported_characters(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'confirm-rename')]").click()

    input_field = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='newName']"))
    )
    input_field.clear()

    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    input_field.send_keys("Pipeline" + spec_char)
    browser.find_element(By.TAG_NAME, "body").click()

    wait5.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-error-area--visible"))
    )
    expected_text = f"‘{spec_char}’ is an unsafe character"
    wait5.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "error"), expected_text)
    )
    error_message = browser.find_element(By.CLASS_NAME, "error").text

    assert error_message == expected_text


def test_availability_of_health_metrics(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'configure') and contains(@class,'task-link')]").click()

    health_metrics_btn = wait5.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "advancedButton"))
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
    health_metrics_btn.click()

    add_metric_btn = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@suffix='healthMetrics']"))
    )
    add_metric_btn.click()

    wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='tippy-2']"))
    )
    child_with_name = browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Child item with the given name')]")
    child_worst_health = browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Child item with worst health')]")
    health_primary_branch = browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Health of the primary branch of a repository')]")

    assert child_with_name.is_enabled() == True
    assert child_worst_health.is_enabled() == True
    assert health_primary_branch.is_enabled() == True


def test_health_metrics_child_item_with_given_name(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'configure') and contains(@class,'task-link')]").click()

    health_metrics_btn = wait5.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "advancedButton"))
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
    health_metrics_btn.click()

    add_metric_btn = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@suffix='healthMetrics']"))
    )
    add_metric_btn.click()

    wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='tippy-2']"))
    )
    browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Child item with the given name')]").click()
    child_name = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='_.childName']"))
    )

    assert child_name.is_displayed() == True


def test_health_metrics_child_item_with_worst_health(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'configure') and contains(@class,'task-link')]").click()

    health_metrics_btn = wait5.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "advancedButton"))
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
    health_metrics_btn.click()

    add_metric_btn = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@suffix='healthMetrics']"))
    )
    add_metric_btn.click()

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='tippy-2']"))
    )
    browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Child item with worst health')]").click()
    wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@descriptorid,'WorstChildHealthMetric')]"))
    )
    recursive_checkbox = browser.find_element(By.XPATH, "//input[@name='_.recursive']")
    assert recursive_checkbox.is_displayed() == True
    assert recursive_checkbox.is_selected() == True


def test_health_metrics_health_of_the_primary_branch(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'configure') and contains(@class,'task-link')]").click()

    health_metrics_btn = wait5.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "advancedButton"))
    )
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
    health_metrics_btn.click()

    add_metric_btn = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@suffix='healthMetrics']"))
    )
    add_metric_btn.click()

    wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='tippy-2']"))
    )
    browser.find_element(By.XPATH, "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                   "and contains(text(),'Health of the primary branch of a repository')]").click()
    primary_branch_metric = wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@descriptorid,'PrimaryBranchHealthMetric')]"))
    )

    assert primary_branch_metric.is_displayed() == True

def test_delete_multibranch_pipeline_via_side_panel(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[@data-title='Delete Multibranch Pipeline']").click()

    dialog = wait5.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "dialog[open]"))
    )
    confirm_btn = dialog.find_element(By.XPATH, ".//button[@data-id='ok']")
    confirm_btn.click()
    wait5.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "dialog[open]"))
    )

    welcome_title = browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")

    assert welcome_title.text == "Welcome to Jenkins!"

def test_cancel_pipeline_deletion(browser, wait5):
    create_multibranch_pipeline(browser, wait5)

    wait5.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'job-index-headline')]"))
    )
    browser.find_element(By.ID, "jenkins-head-icon").click()

    link_selector = f"//a[@href='job/{PIPELINE_NAME}/' and contains(@class,'jenkins-table__link')]"
    browser.find_element(By.XPATH, link_selector).click()

    wait5.until(
        EC.visibility_of_element_located((By.ID, "side-panel"))
    )
    browser.find_element(By.XPATH, "//a[@data-title='Delete Multibranch Pipeline']").click()

    dialog = wait5.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "dialog[open]"))
    )
    cancel_btn = dialog.find_element(By.XPATH, ".//button[@data-id='cancel']")
    cancel_btn.click()

    title = browser.find_element(By.XPATH, "//h1[contains(@class,'job-index-headline')]")

    assert title.text == PIPELINE_NAME
    assert f"job/{PIPELINE_NAME}/" in browser.current_url
