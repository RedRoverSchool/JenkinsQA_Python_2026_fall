import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.home_page import HomePage

TEST_TEXT = 'random_name'
TEXT_AFTER = 'test_text'
MULTILINE_TEXT = "Первая строка\nВторая строка\nТретья строка"
CREATE_ITEM_BTN = (By.XPATH, "//*[@id='tasks']/div[1]/span/a")
ITEM_NAME_FLD = (By.XPATH, "//*[@id='name']")
PIPELINE_BTN = (By.XPATH, "//*[@id='items']/div[1]/label")
OK_BTN = (By.XPATH, "//*[@id='ok-button']")
DESCRIPTION_FLD = (By.XPATH, "//textarea[@name='description']")
SAVE_BTN = (By.XPATH, "//*[@id='bottom-sticker']/div/button[1]")
DESCRIPTION_CONTENT_FLD = (By.XPATH, "//*[@id='description-content']")
EDIT_DESCRIPTION_BTN = (By.XPATH, "//*[@id='description-link']/span")
DESCRIPTION_TEXTAREA_FLD = (By.XPATH, "//*[@id='description-textarea']")
SAVE_BTN_OK = (By.XPATH, "//button[@data-id='ok']")
PIPELINE_LINK = (By.XPATH, f"//a[contains(@href, 'job/{TEST_TEXT}')]")
JOB_NAME = (By.XPATH, "//*[@id='job_random_name']/td[3]/a/span")
DROPDOWN_CHEVRON = (By.XPATH, f"//*[@id='job_random_name']/td[3]/a/button")
DROPDOWN_CONFIGURE = (By.XPATH, "//*[@id='tippy-4']/div/div/div/a[2]")
PREVIEW_BTN = (By.XPATH, "//*[@id='jenkins']/dialog[2]/div[2]/form/div[1]/div/div[1]/div[1]/a[1]")
PREVIEW_FLD = (By.XPATH, "//*[@id='jenkins']/dialog[2]/div[2]/form/div[1]/div/div[1]/div[2]")


@pytest.mark.dependency()
def test_access_description_via_new_item(browser, wait10):
    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(TEST_TEXT)
        .select_pipeline_and_click_ok()
    )
    configuration_page.enter_description(TEST_TEXT)
    assert configuration_page.get_description_value() == TEST_TEXT


@pytest.mark.dependency(depends=["test_access_description_via_new_item"])
def test_access_description_via_click_pipeline_name(browser, wait10):
    actual_text = (
        HomePage(browser)
        .click_pipeline(TEST_TEXT)
        .click_add_or_rename_description_btn()
        .click_clear_and_send_keys_in_field_area(DESCRIPTION_TEXTAREA_FLD, TEXT_AFTER)
        .click_btn(SAVE_BTN_OK)
        .wait_for_text_in_element(DESCRIPTION_CONTENT_FLD, TEXT_AFTER)
        .get_element_text(DESCRIPTION_CONTENT_FLD)
    )
    assert actual_text == TEXT_AFTER, f"Ожидался текст '{TEXT_AFTER}', но получен '{actual_text}'"

@pytest.mark.dependency(depends=["test_access_description_via_click_pipeline_name"])
def test_edit_existing_description(browser, wait10):
    text_after = (
        HomePage(browser)
        .click_pipeline(TEST_TEXT)
        .click_add_or_rename_description_btn()
        .click_clear_and_send_keys_in_field_area(DESCRIPTION_TEXTAREA_FLD, TEST_TEXT)
        .click_btn(SAVE_BTN_OK)
        .wait_for_text_in_element(DESCRIPTION_CONTENT_FLD, TEST_TEXT)
        .get_element_text(DESCRIPTION_CONTENT_FLD)
    )
    assert text_after == TEST_TEXT, f"Ожидался {TEST_TEXT}, а получен {text_after}"


def test_enter_multiline_description_on_configure(browser, wait10):
    actual_result = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(TEST_TEXT)
        .select_pipeline_and_click_ok()
        .enter_description(MULTILINE_TEXT)
        .click_btn(SAVE_BTN)
        .get_element_text(DESCRIPTION_CONTENT_FLD)
    )
    lines = actual_result.splitlines()
    assert len(lines) == 3, f"Ожидалось 3 строки, а получено {len(lines)}"


@pytest.mark.dependency(depends=["test_access_description_via_click_pipeline_name"])
def test_clear_description_field(browser, wait10):

    wait10.until(EC.element_to_be_clickable(PIPELINE_LINK)).click()
    desc_content = browser.find_element(*EDIT_DESCRIPTION_BTN)
    desc_content.click()

    desc_textarea = browser.find_element(*DESCRIPTION_TEXTAREA_FLD)
    desc_textarea.send_keys(Keys.CONTROL, "a")
    desc_textarea.send_keys(Keys.BACKSPACE)

    save_btn_2 = browser.find_element(*SAVE_BTN_OK)
    save_btn_2.click()

    def description_is_empty(driver):
        elements = driver.find_elements(*DESCRIPTION_CONTENT_FLD)
        if len(elements) == 0:
            return True
        return elements[0].text.strip() == ""

    wait10.until(description_is_empty)
    assert description_is_empty(browser), "Ошибка: блок с описанием не пустой"

@pytest.mark.skip
@pytest.mark.dependency(depends=["test_access_description_via_new_item"])
def test_description_via_drop_down_menu(browser, wait10):
    job_name = browser.find_element(*JOB_NAME)
    actions = ActionChains(browser)
    actions.move_to_element(job_name)
    actions.perform()
    chevron = wait10.until(EC.visibility_of_element_located(DROPDOWN_CHEVRON))
    chevron.click()
    configue = wait10.until(EC.element_to_be_clickable(DROPDOWN_CONFIGURE))
    configue.click()
    wait10.until(EC.url_contains(TEST_TEXT))
    wait10.until(EC.url_contains("configure"))
    desc = wait10.until(EC.element_to_be_clickable(DESCRIPTION_FLD))
    desc.click()
    desc.clear()
    desc.send_keys(TEST_TEXT)
    wait10.until(EC.text_to_be_present_in_element_value(DESCRIPTION_FLD, TEST_TEXT))
    assert desc.get_attribute('value') == TEST_TEXT, desc.get_attribute("value")


@pytest.mark.dependency(depends=["test_access_description_via_click_pipeline_name"])
def test_preview_description(browser, wait10):
    wait10.until(EC.element_to_be_clickable(PIPELINE_LINK)).click()
    edit_desc_btn = browser.find_element(*EDIT_DESCRIPTION_BTN)
    edit_desc_btn.click()
    desc_textarea_fld = browser.find_element(*DESCRIPTION_TEXTAREA_FLD)
    desc_textarea_fld.click()
    desc_textarea_fld.clear()
    desc_textarea_fld.send_keys(TEST_TEXT)
    preview_btn = browser.find_element(*PREVIEW_BTN)
    preview_btn.click()
    preview_fld = browser.find_element(*PREVIEW_FLD)
    wait10.until(EC.text_to_be_present_in_element(PREVIEW_FLD, TEST_TEXT))
    text = preview_fld.text
    assert text == TEST_TEXT

