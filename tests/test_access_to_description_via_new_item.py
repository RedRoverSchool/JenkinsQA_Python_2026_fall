import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def wait(browser):
    wait = WebDriverWait(browser, timeout=10)
    return wait

CREATE_ITEM_BTN = (By.XPATH, "//*[@id='tasks']/div[1]/span/a")
ITEM_NAME_FLD = (By.XPATH, "//*[@id='name']")
PIPELINE_BTN = (By.XPATH, "//*[@id='items']/div[1]/label")
OK_BTN = (By.XPATH, "//*[@id='ok-button']")
DESCRIPTION_FLD = (By.XPATH, "//*[@id='main-panel']/form/div[1]/div[2]/div/div[2]/textarea")
TEST_TEXT = 'random_name'


def test_access_to_description_via_new_item(browser, wait):

    wait.until(EC.element_to_be_clickable(CREATE_ITEM_BTN)).click()
    name_fld = wait.until(EC.visibility_of_element_located(ITEM_NAME_FLD))
    name_fld.click()
    name_fld.send_keys(TEST_TEXT)
    wait.until(EC.element_to_be_clickable(PIPELINE_BTN)).click()
    wait.until(EC.element_to_be_clickable(OK_BTN)).click()
    wait.until(EC.url_contains("random_name"))
    wait.until(EC.url_contains("configure"))
    desc = wait.until(EC.visibility_of_element_located(DESCRIPTION_FLD))
    desc.click()
    desc.clear()
    desc.send_keys(TEST_TEXT)
    assert desc.get_attribute('value') == TEST_TEXT, desc.get_attribute("value")

