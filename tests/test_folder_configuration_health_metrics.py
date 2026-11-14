import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

TEST_TEXT = 'random_name'
NEW_ITEM = (By.XPATH, "//*[@id='tasks']/div[1]/span/a")
ITEM_NAME_FLD = (By.XPATH, "//*[@id='name']")
FOLDER_BTN = (By.XPATH, "//*[@id='items']/div[4]/label")
OK_BTN = (By.XPATH, "//*[@id='ok-button']")
HEALTH_BTN = (By.XPATH, "(//button[contains(., 'Health metrics')])[2]")
ADD_METRIC_BTN = (By.XPATH, "//button[contains(., 'Add metric')]")


def test_access_health_metrics_section(browser, wait10):
    actions = ActionChains(browser)
    new_item = browser.find_element(*NEW_ITEM)
    new_item.click()
    item_name_fld = browser.find_element(*ITEM_NAME_FLD)
    item_name_fld.click()
    item_name_fld.clear()
    item_name_fld.send_keys(TEST_TEXT)
    folder_btn = browser.find_element(*FOLDER_BTN)
    folder_btn.click()
    ok_btn = browser.find_element(*OK_BTN)
    ok_btn.click()
    wait10.until(EC.url_contains(TEST_TEXT))
    wait10.until(EC.url_contains("configure"))
    health_btn = wait10.until(EC.visibility_of_element_located(HEALTH_BTN))
    actions.move_to_element(health_btn).click().perform()
    add_metric_btn = browser.find_element(*ADD_METRIC_BTN)
    assert add_metric_btn.is_displayed(), "Кнопка 'Add metric' не видна"
    assert add_metric_btn.is_enabled(), "Кнопка 'Add metric' не активна"








