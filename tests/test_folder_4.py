import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage


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


@pytest.mark.parametrize('invalid_characters', ['!', '@', '%', '&'])
def test_create_folder_with_invalid_characters_name(browser, invalid_characters):
    invalid_name = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(f'{ITEM_NAME}{invalid_characters}')
        .is_ok_button_enabled()

    )

    assert not invalid_name

