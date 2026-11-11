import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

FOLDER_NAME = "Test_Folder"
NEW_ITEM_BUTTON = (By.CSS_SELECTOR, 'a[href="newJob"]')
FOLDER_NAME_INPUT = (By.CSS_SELECTOR, '#name')
FOLDER_OPTION = (By.XPATH, "//span[normalize-space()='Folder']")
SUBMIT_ITEM_BUTTON = (By.CSS_SELECTOR, '.jenkins-button.jenkins-button--primary.jenkins-buttons-row--equal-width')
SAVE_FOLDER_BUTTON = (By.CSS_SELECTOR,'.jenkins-button.jenkins-submit-button.jenkins-button--primary')
FOLDER_HEADER = (By.CSS_SELECTOR, 'h1')
ERROR_AREA = (By.CSS_SELECTOR, '.validation-error-area.validation-error-area--visible')

@pytest.fixture
def empty_name_on_new_item_page(browser, wait10):
    wait10.until(EC.element_to_be_clickable(NEW_ITEM_BUTTON))
    browser.find_element(*NEW_ITEM_BUTTON).click()
    browser.find_element(*FOLDER_OPTION).click()

@pytest.fixture
def created_folder(browser, wait10, empty_name_on_new_item_page):
    browser.find_element(*FOLDER_NAME_INPUT).send_keys(FOLDER_NAME)
    browser.find_element(*SUBMIT_ITEM_BUTTON).click()
    browser.find_element(*SAVE_FOLDER_BUTTON).click()
    wait10.until(EC.url_contains(FOLDER_NAME))

def test_create(browser, wait10, empty_name_on_new_item_page):
    browser.find_element(*FOLDER_NAME_INPUT).send_keys(FOLDER_NAME)
    wait10.until(EC.element_to_be_clickable(SUBMIT_ITEM_BUTTON))
    browser.find_element(*SUBMIT_ITEM_BUTTON).click()
    wait10.until(EC.element_to_be_clickable(SAVE_FOLDER_BUTTON))
    browser.find_element(*SAVE_FOLDER_BUTTON).click()
    wait10.until(EC.url_contains(FOLDER_NAME))

def test_create_with_empty_name(browser, wait10, empty_name_on_new_item_page):
    assert not browser.find_element(*SUBMIT_ITEM_BUTTON).is_enabled()

def test_create_with_empty_name_error(browser, wait10, empty_name_on_new_item_page):
    browser.find_element(*FOLDER_NAME_INPUT).send_keys(FOLDER_NAME)
    wait10.until(EC.element_to_be_clickable(SUBMIT_ITEM_BUTTON))
    browser.find_element(*FOLDER_NAME_INPUT).clear()
    wait10.until(EC.visibility_of_element_located(ERROR_AREA))

    assert browser.find_element(*ERROR_AREA).text == 'Поле не может быть пустым, введите имя'

@pytest.mark.parametrize("symbols", ['A', 'ф', '1', 'te st', ' test ', ',', '"', "'"])
def test_name_is_valid(browser, wait10, symbols, empty_name_on_new_item_page):
    browser.find_element(*FOLDER_NAME_INPUT).send_keys(symbols)
    wait10.until(EC.element_to_be_clickable(SUBMIT_ITEM_BUTTON))

    assert browser.find_element(*SUBMIT_ITEM_BUTTON).is_enabled()

@pytest.mark.parametrize("symbols", ['/', '\\', '?', '*', ':', '|', '>', '<'])
def test_name_is_invalid(browser, wait10, symbols, empty_name_on_new_item_page):
    browser.find_element(*FOLDER_NAME_INPUT).send_keys(symbols)
    wait10.until(EC.visibility_of_element_located(ERROR_AREA))
    errors = (f'"{symbols}" is not an allowed name', f"'{symbols}' небезопасный символ")

    assert browser.find_element(*ERROR_AREA).text in errors