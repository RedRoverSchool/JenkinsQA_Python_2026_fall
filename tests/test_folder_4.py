import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.new_item_page import NewItemPage


ITEM_NAME = 'folder_name'
DISPLAY_NAME = 'display_name'
DISCRIPTION_TEXT = 'description'

def test_create_item_folder(browser,wait5,wait10):

    progect_name = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(ITEM_NAME)
        .select_folder_and_click_ok()
        .set_display_name(DISPLAY_NAME)
        .set_dicription(DISCRIPTION_TEXT)
        .click_submit()

    )

    assert browser.find_element(By.XPATH, "//h1[@class='job-index-headline page-headline']").is_displayed()


def test_create_item_folder_with_empty_name(browser,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_type_folder = browser.find_element(By.XPATH, "//span[text()='Folder']")
    item_type_folder.click()
    button_ok = browser.find_element(By.XPATH, "//button[@id='ok-button']")
    assert not button_ok.is_enabled()


@pytest.mark.parametrize('invalid_characters',['/','!','?','&','*','>'])
def test_create_item_folder_with_empty_invalid_characters_in_name(browser,invalid_characters,wait5,wait10):
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()
    item_name_fild = wait5.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']")))
    item_name_fild.send_keys(invalid_characters)
    error = wait5.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='error']")))
    assert error.is_displayed()