import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

TEST_TEXT = 'random_name'
TEXT_AFTER = 'test_text'
CREATE_ITEM_BTN = (By.XPATH, "//*[@id='tasks']/div[1]/span/a")
ITEM_NAME_FLD = (By.XPATH, "//*[@id='name']")
PIPELINE_BTN = (By.XPATH, "//*[@id='items']/div[1]/label")
OK_BTN = (By.XPATH, "//*[@id='ok-button']")
DESCRIPTION_FLD = (By.XPATH, "//*[@id='main-panel']/form/div[1]/div[2]/div/div[2]/textarea")
SAVE_BTN_1 = (By.XPATH, "//*[@id='bottom-sticker']/div/button[1]")
DESCRIPTION_CONTENT_FLD = (By.XPATH, "//*[@id='description-content']")
EDIT_DESCRIPTION_BTN = (By.XPATH, "//*[@id='description-link']/span")
DESCRIPTION_TEXTAREA_FLD = (By.XPATH, "//*[@id='description-textarea']")
SAVE_BTN_2 = (By.XPATH, "//*[@id='bottom-sticker']/div/button[2]")
PIPELINE_LINK = (By.XPATH, f"//a[contains(@href, 'job/{TEST_TEXT}')]")



@pytest.mark.dependency()
def test_access_description_via_new_item(browser, wait10):

    wait10.until(EC.element_to_be_clickable(CREATE_ITEM_BTN)).click()
    name_fld = wait10.until(EC.visibility_of_element_located(ITEM_NAME_FLD))
    name_fld.click()
    name_fld.clear()
    name_fld.send_keys(TEST_TEXT)
    pip_btn = browser.find_element(*PIPELINE_BTN)
    pip_btn.click()
    ok_btn = browser.find_element(*OK_BTN)
    ok_btn.click()
    wait10.until(EC.url_contains(TEST_TEXT))
    wait10.until(EC.url_contains("configure"))
    desc = browser.find_element(*DESCRIPTION_FLD)
    desc.click()
    desc.clear()
    desc.send_keys(TEST_TEXT)
    assert desc.get_attribute('value') == TEST_TEXT, desc.get_attribute("value")


@pytest.mark.dependency(depends=["test_access_description_via_new_item"])
def test_access_description_via_click_pipeline_name(browser, wait10):

    wait10.until(EC.element_to_be_clickable(PIPELINE_LINK)).click()
    edit_desc_btm = wait10.until(EC.element_to_be_clickable(EDIT_DESCRIPTION_BTN))
    edit_desc_btm.click()
    desc_textarea = wait10.until(EC.visibility_of_element_located(DESCRIPTION_TEXTAREA_FLD))
    desc_textarea.click()
    desc_textarea.clear()
    desc_textarea.send_keys(TEXT_AFTER)
    save_btn_2 = browser.find_element(*SAVE_BTN_2)
    save_btn_2.click()
    wait10.until(EC.text_to_be_present_in_element(DESCRIPTION_CONTENT_FLD, TEXT_AFTER))
    desc_content_fld = browser.find_element(*DESCRIPTION_CONTENT_FLD)
    actual_text = desc_content_fld.text.strip()
    assert actual_text == TEXT_AFTER, f"Ожидался текст '{TEXT_AFTER}', но получен '{actual_text}'"

@pytest.mark.dependency(depends=["test_access_description_via_click_pipeline_name"])
def test_edit_existing_description(browser, wait10):
    wait10.until(EC.element_to_be_clickable(PIPELINE_LINK)).click()
    edit_desc_btn = browser.find_element(*EDIT_DESCRIPTION_BTN)
    edit_desc_btn.click()
    desc_textarea_fld = browser.find_element(*DESCRIPTION_TEXTAREA_FLD)
    desc_textarea_fld.click()
    desc_textarea_fld.clear()
    desc_textarea_fld.send_keys(TEST_TEXT)
    save_btn_edit = browser.find_element(*SAVE_BTN_2)
    save_btn_edit.click()
    wait10.until(EC.text_to_be_present_in_element(DESCRIPTION_CONTENT_FLD, TEST_TEXT))
    desc_content_fld = browser.find_element(*DESCRIPTION_CONTENT_FLD)
    text_after = desc_content_fld.text.strip()
    assert text_after == TEST_TEXT, f"Ожидался {TEST_TEXT}, а получен {text_after}"



