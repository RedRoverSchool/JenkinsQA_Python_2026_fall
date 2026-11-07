import pytest
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


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
        EC.element_to_be_clickable((By.ID, "ok-button"))
    )
    browser.execute_script("arguments[0].click();", ok_button)


    WebDriverWait(browser, 10).until(EC.url_contains("/configure"))
    assert "/configure" in browser.current_url


    # save_button = WebDriverWait(browser, timeout=10).until(
    #     EC.element_to_be_clickable((By.NAME, "Submit"))
    # )
    # save_button.click()
    # jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[./span[text()='Jenkins']]")))
    # browser.execute_script("arguments[0].click();", jenkins_logo)

    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo")))
    jenkins_logo.click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    print(f"Создана папке - {FOLDER_NAME}")
    folder_data = {"name": FOLDER_NAME,}
    yield folder_data
    CURRENT_FOLDER_NAME = folder_data["name"]
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

def test_create_and_verify_if_the_folder_was_created(browser, create_folder):
    FOLDER_NAME = create_folder["name"]
    folder_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert folder_element.is_displayed(), f"Ошибка: Созданная папка '{FOLDER_NAME}' не отображается на странице!"


def test_verify_renaming_with_a_valid_name(browser, create_folder):
    FOLDER_NAME = create_folder["name"]
    folder_link  = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//a[@href='job/{FOLDER_NAME}/']"))
    )
    print(f"Папка с именем - {FOLDER_NAME} найдена")
    folder_link.click()
    print(f"Произошел клик по папке - {FOLDER_NAME}")
    configure_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='task-link-text' and text()='Configure']/..")))
    configure_button.click()
    NEW_NAME = f"Updated-{FOLDER_NAME}"
    create_folder["name"] = NEW_NAME
    print(f"Новое имя - {NEW_NAME}")
    input_display_name = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='setting-main']//input[@checkurl]")))
    input_display_name.send_keys(NEW_NAME)
    time.sleep(2)
    save_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@formnovalidate='formNoValidate']")))
    browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
    save_button.click()
    WebDriverWait(browser, 10).until(
        EC.staleness_of(save_button)
    )
    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".app-jenkins-logo")))
    jenkins_logo.click()
    folder_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-href*='{FOLDER_NAME}']"))
    )
    assert f"{NEW_NAME}" in browser.page_source, f"Ошибка: Обновленное имя папки '{NEW_NAME}' не отображается на странице!"











