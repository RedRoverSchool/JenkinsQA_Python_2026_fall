import pytest
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def create_folder(browser):
    FOLDER_NAME = f"Folder_{random.randint(0,1000)}"
    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    input_name_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='name']"))
    )
    input_name_field.send_keys(FOLDER_NAME)


    item_type_folder = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Folder']"))
    )
    item_type_folder.click()

    ok_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "ok-button"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", ok_button)
    ok_button.click()


    save_button = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable((By.NAME, "Submit"))
    )
    save_button.click()
    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo")))
    jenkins_logo.click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    print(f"Создана папке - {FOLDER_NAME}")
    yield FOLDER_NAME
    try:
        browser.get(f"http://localhost:8080/job/{FOLDER_NAME}/")
        delete_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-title='Delete Folder']")))
        delete_button.click()
        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present())
            browser.switch_to.alert.accept()
        except:
            ok_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-id='ok' and contains(text(), 'Yes')]"))
            )
            ok_button.click()
        print(f"Удалена папка - {FOLDER_NAME}")
    except WebDriverException as e:
        print(f"Не удалось автоматически удалить папку {FOLDER_NAME}")
@pytest.mark.skip
def test_create_and_verify_if_the_folder_was_created2(browser, create_folder):
    FOLDER_NAME = create_folder
    folder_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert folder_element.is_displayed(), f"Ошибка: Созданная папка '{FOLDER_NAME}' не отображается на странице!"
@pytest.mark.skip
def test_create_and_verify_if_the_folder_was_created(browser):
    wait = WebDriverWait(browser, 10)
    FOLDER_NAME = f"Folder_{random.randint(0,1000)}"
    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    input_name_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='name']"))
    )
    input_name_field.send_keys(FOLDER_NAME)


    item_type_folder = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Folder']"))
    )
    item_type_folder.click()

    ok_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", ok_button)
    ok_button.click()


    save_button = WebDriverWait(browser, timeout=10).until(
        EC.element_to_be_clickable((By.NAME, "Submit"))
    )
    save_button.click()

    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo")))
    jenkins_logo.click()

    folder_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert folder_element.is_displayed(), f"Ошибка: Созданная папка '{FOLDER_NAME}' не отображается на странице!"












