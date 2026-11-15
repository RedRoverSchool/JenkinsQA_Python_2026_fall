import re
import pytest
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PIPELINE_NAME = "Pipeline 1"
QP_POSITIVE = "10"
QP_NEGATIVE = "-2"
NON_INTEGER = "5.5"
NEGATIVE_ERROR = "This value should be larger than 0"
NON_INTEGER_ERROR = "Not an integer"


def test_quiet_period_accepts_positive_integer(browser, wait5, wait2):
    create_pipeline(browser, wait2)
    set_quiet_period(browser, wait5, QP_POSITIVE)
    browser.find_element(By.CSS_SELECTOR, "button[name='Submit']").click()
    wait5.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$='configure']"))).click()
    open_advanced_dropdown(browser)
    quiet_period_seconds = browser.find_element(By.CSS_SELECTOR, "input[name='quiet_period']").get_attribute("value")

    assert quiet_period_seconds == QP_POSITIVE


@pytest.mark.parametrize("value,expected_error", [
    pytest.param(QP_NEGATIVE, NEGATIVE_ERROR, id="negative_integer_value"),
    pytest.param(NON_INTEGER, NON_INTEGER_ERROR, id="non_integer_value"),
])
def test_quiet_period_rejects_negative_and_non_integer_values(browser, wait5, wait2, value, expected_error):
    create_pipeline(browser, wait2)
    set_quiet_period(browser, wait5, value)
    error = wait5.until(EC.visibility_of_element_located((
        By.XPATH,
        "//input[@name='quiet_period']/ancestor::div[contains(@class,'jenkins-form-item')]/descendant::div[@class='error']"
    ))).text

    assert error == expected_error


@pytest.mark.parametrize("value", [
    pytest.param("AbCdeEГд", id="letters_as_value"),
    pytest.param("!@#$%^&*()", id="symbols_as_value"),
    pytest.param("A512@d", id="mix_value"),
])
def test_quiet_period_letters_and_symbols_can_not_be_entered(browser, wait2, wait5, value):
    create_pipeline(browser, wait2)
    set_quiet_period(browser, wait5, value)
    input_field = browser.find_element(By.CSS_SELECTOR, "input[name='quiet_period']").get_property("value")
    input_expected = re.sub(r"[^0-9]", "", value)

    assert input_field == input_expected


def create_pipeline(browser, wait2):
    wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view/all/newJob']"))).click()
    wait2.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[value='org.jenkinsci.plugins.workflow.job.WorkflowJob'] + span"))).click()
    browser.find_element(By.ID, "name").send_keys(PIPELINE_NAME)
    browser.find_element(By.ID, "ok-button").click()


def set_quiet_period(browser, wait5, seconds):
    open_advanced_dropdown(browser)
    wait5.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='hasCustomQuietPeriod'] + label"))).click()
    quiet_period_seconds = browser.find_element(By.CSS_SELECTOR, "input[name='quiet_period']")
    quiet_period_seconds.clear()
    quiet_period_seconds.send_keys(seconds)
    quiet_period_seconds.send_keys(Keys.TAB)


def open_advanced_dropdown(browser):
    wait = WebDriverWait(browser, 6)
    max_attempts = 2
    for attempt in range(max_attempts):
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Advanced')]/ancestor::button"))).click()
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".jenkins-bottom-app-bar__shadow--stuck")))
            break
        except TimeoutException as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    f"After {max_attempts} clicks on the left sidebar, the page failed to scroll to the bottom. Save is obstructing Advanced."
                ) from e
    browser.find_element(By.CSS_SELECTOR, ".jenkins-section button.advancedButton").click()
