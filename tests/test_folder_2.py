import pytest
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def create_folder(browser, wait10, wait5):
    FOLDER_NAME = f"Folder_{random.randint(0,1000)}"
    create_item_button = browser.find_element(By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/..")
    create_item_button.click()

    input_name_field = browser.find_element(By.XPATH, "//input[@name='name']")
    input_name_field.send_keys(FOLDER_NAME)

    item_type_folder = browser.find_element(By.XPATH, "//span[text()='Folder']")
    item_type_folder.click()

    ok_button = wait10.until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    browser.execute_script("arguments[0].click();", ok_button)


    wait10.until(EC.url_contains("/configure"))
    assert "/configure" in browser.current_url

    jenkins_logo = browser.find_element(By.CSS_SELECTOR, ".app-jenkins-logo")
    jenkins_logo.click()

    wait10.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    print(f"Создана папке - {FOLDER_NAME}")
    folder_data = {"name": FOLDER_NAME,}
    yield folder_data

    try:
        browser.get(f"http://localhost:8080/job/{FOLDER_NAME}/")
        delete_button = wait5.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-title='Delete Folder']")))
        delete_button.click()
        try:
            wait5.until(EC.alert_is_present())
            browser.switch_to.alert.accept()
        except:
            ok_button = wait5.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-id='ok' and contains(text(), 'Yes')]"))
            )
            ok_button.click()
        print(f"Удалена папка - {FOLDER_NAME}")
    except WebDriverException as e:
        print(f"Не удалось автоматически удалить папку {FOLDER_NAME}")

def test_create_and_verify_if_the_folder_was_created(browser, create_folder, wait10):
    FOLDER_NAME = create_folder["name"]
    folder_element = wait10.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert folder_element.is_displayed(), f"Ошибка: Созданная папка '{FOLDER_NAME}' не отображается на странице!"


def test_verify_renaming_with_a_valid_name(browser, create_folder, wait10):
    FOLDER_NAME = create_folder["name"]
    folder_link  = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//a[@href='job/{FOLDER_NAME}/']"))
    )
    folder_link.click()
    configure_button = browser.find_element(By.XPATH, "//span[@class='task-link-text' and text()='Configure']/..")
    configure_button.click()
    NEW_NAME = f"Updated-{FOLDER_NAME}"
    create_folder["name"] = NEW_NAME
    input_display_name = browser.find_element(By.XPATH, "//*[@class='setting-main']//input[@checkurl]")
    input_display_name.send_keys(NEW_NAME)
    save_button = browser.find_element(By.XPATH, "//button[@formnovalidate='formNoValidate']")
    browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
    save_button.click()
    wait10.until(
        EC.staleness_of(save_button)
    )
    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo")))
    jenkins_logo.click()

    assert f"{NEW_NAME}" in browser.page_source, f"Ошибка: Обновленное имя папки '{NEW_NAME}' не отображается на странице!"


def test_verify_error_message_and_red_highlight_on_duplicate_name(browser, create_folder, wait10):
    FOLDER_NAME = create_folder["name"]
    ERROR_MESSAGE = f"A job already exists with the name ‘{FOLDER_NAME}’"
    ADD_NEW_ITEM = browser.find_element(By.CSS_SELECTOR, '[href="/view/all/newJob"]')
    ADD_NEW_ITEM.click()
    input_name_field = browser.find_element(By.XPATH, "//input[@name='name']")
    input_name_field.send_keys(FOLDER_NAME)
    red_bordered_input_field = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='validation-error-area--visible']")))
    text_found = WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*='validation-error-area--visible']"), ERROR_MESSAGE))

    assert red_bordered_input_field.is_displayed() and text_found, "Expected error message did nit appear under the input field"









