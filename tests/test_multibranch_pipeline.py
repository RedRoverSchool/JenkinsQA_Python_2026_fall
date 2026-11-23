import secrets
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.base_item_page import BaseItemPage

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

@pytest.fixture
def created_multibranch_pipeline(browser):
    (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PIPELINE_NAME)
        .select_multibranch_and_click_ok()
        .goto_home_page()
    )


def test_create_multibranch_pipeline(browser, created_multibranch_pipeline):
    pipeline_name = HomePage(browser).get_first_project_name()

    assert PIPELINE_NAME == pipeline_name


def test_return_to_the_dashboard_without_creating_multibranch_pipeline(browser):
    page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PIPELINE_NAME)
        .select_multibranch()
        .goto_home_page()
    )

    welcome_title = page.get_welcome_title()
    assert welcome_title == "Welcome to Jenkins!"


def test_multibranch_with_special_characters(browser):
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)
    pipeline_name = "Pipeline" + spec_char

    page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(pipeline_name)
        .select_multibranch()
    )

    expected_text = f"‘{spec_char}’ is an unsafe character"

    assert page.is_ok_button_disabled()
    assert page.get_error_name_message() == expected_text


def test_rename_multibranch_pipeline_from_dropdown_menu(browser, created_multibranch_pipeline):
    home_page = HomePage(browser)
    project_name = home_page.get_first_project_name()
    new_name = "Pipeline_2"

    item_page = (home_page
     .click_project_context_menu_and_click_rename(project_name)
     .rename_to(new_name)
     )

    assert item_page.get_item_name() == new_name
    assert f"job/{new_name}" in browser.current_url


def test_rename_multibranch_pipeline_from_project_menu(browser, created_multibranch_pipeline):
    home_page = HomePage(browser)
    project_name = home_page.get_first_project_name()
    new_name = "Pipeline_2"

    item_page = (home_page
                 .click_job(project_name)
                 .click_rename()
                 .rename_to(new_name)
                 )

    assert item_page.get_item_name() == new_name
    assert f"job/{new_name}" in browser.current_url


def test_rename_multibranch_pipeline_with_same_name(browser, created_multibranch_pipeline):
    home_page = HomePage(browser)
    project_name = home_page.get_first_project_name()

    error_page = (home_page
                 .click_job(project_name)
                 .click_rename()
                 .try_rename_to(PIPELINE_NAME)
                 )

    expected_text = "The new name is the same as the current name."
    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text

@pytest.mark.skip()
def test_rename_multibranch_pipeline_with_blank_name(browser, created_multibranch_pipeline):
    home_page = HomePage(browser)
    project_name = home_page.get_first_project_name()

    error_page = (home_page
                  .click_job(project_name)
                  .click_rename()
                  .try_rename_to()
                  )

    expected_text = "No name is specified"
    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text


def test_rename_multibranch_pipeline_with_unsupported_characters(browser, created_multibranch_pipeline):
    home_page = HomePage(browser)
    project_name = home_page.get_first_project_name()
    spec_chars = r"!@#$%^&*[]<>;:/\|"
    spec_char = secrets.choice(spec_chars)

    error_page = (home_page
                  .click_job(project_name)
                  .click_rename()
                  .try_rename_to("Pipeline" + spec_char)
                  )

    expected_text = f"‘{spec_char}’ is an unsafe character"
    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == expected_text


def test_availability_of_health_metrics(browser, wait5, created_multibranch_pipeline):
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
    health_primary_branch = browser.find_element(By.XPATH,
                                                 "//div[@id='tippy-2']//button[@class='jenkins-dropdown__item' "
                                                 "and contains(text(),'Health of the primary branch of a repository')]")

    assert child_with_name.is_enabled() == True
    assert child_worst_health.is_enabled() == True
    assert health_primary_branch.is_enabled() == True


def test_health_metrics_child_item_with_given_name(browser, wait5, created_multibranch_pipeline):
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


def test_health_metrics_child_item_with_worst_health(browser, wait5, created_multibranch_pipeline):
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


def test_health_metrics_health_of_the_primary_branch(browser, wait5, created_multibranch_pipeline):
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


def test_all_health_metrics_are_added(browser, wait5, created_multibranch_pipeline):
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

    add_metric_locator = (By.XPATH, "//button[@suffix='healthMetrics']")
    add_metric_btn = wait5.until(
        EC.element_to_be_clickable(add_metric_locator)
    )

    metrics = ["Child item with the given name",
               "Child item with worst health",
               "Health of the primary branch of a repository"]

    for metric in metrics:
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_metric_btn)
        wait5.until(
            EC.element_to_be_clickable(add_metric_locator)
        ).click()

        option_locator = (By.XPATH, f"//button[contains(@class, 'jenkins-dropdown__item') "
                                    f"and contains(., '{metric}')]")
        wait5.until(
            EC.element_to_be_clickable(option_locator)
        ).click()

    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_metric_btn)
    wait5.until_not(
        EC.element_to_be_clickable(add_metric_locator)
    )

    assert not add_metric_btn.is_enabled()


def test_delete_multibranch_pipeline_via_side_panel(browser, wait5, created_multibranch_pipeline):
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


def test_cancel_pipeline_deletion(browser, wait5, created_multibranch_pipeline):
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
