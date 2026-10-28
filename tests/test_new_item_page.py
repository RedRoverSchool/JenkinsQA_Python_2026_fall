import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class NewItemPageLocator:
    JENKINS_LOGO = (By.CSS_SELECTOR, ".app-jenkins-logo")
    ADD_NEW_ITEM = (By.CSS_SELECTOR, '[href="/view/all/newJob"]')
    PIPELINE = (By.XPATH, '//*[text()="Pipeline"]')
    FREESTYLE_PROJECT = (By.XPATH, '//*[text()="Freestyle project"]')
    MULTI_CONFIGURATION_PROJECT = (By.XPATH, '//*[text()="Multi-configuration project"]')
    FOLDER = (By.XPATH, '//*[text()="Folder"]')
    MULTIBRANCH_PIPELINE = (By.XPATH, '//*[text()="Multibranch Pipeline"]')
    ORGANIZATION_FOLDER = (By.XPATH, '//*[text()="Organization Folder"]')
    OK_BUTTON = (By.CSS_SELECTOR, "#ok-button")
    ITEM_NAME_INPUT = (By.ID, "name")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error")


UNIQUE_ITEM_NAME = "TC_01.004.002_item"


class MainPageLocator:
    DELETE_BUTTON = (By.XPATH, '//button[contains(@class, "jenkins-dropdown__item") '
                               'and .//*[contains(@class, "icon-edit-delete")]]')
    YES_BUTTON = (By.CSS_SELECTOR, 'button[data-id="ok"]')
    CREATED_ITEM_ROW = (By.CSS_SELECTOR, f'tr[id="job_{UNIQUE_ITEM_NAME}"]')
    DROPDOWN_OPTIONS = (By.CSS_SELECTOR, f'tr[id="job_{UNIQUE_ITEM_NAME}"] .jenkins-menu-dropdown-chevron')
    ITEM_NAME_ROW = (By.CSS_SELECTOR, f'tr[id="job_{UNIQUE_ITEM_NAME}"]')


@allure.description_html("Automated by: <strong>Konstantin Kurilo</strong>")
@allure.title("TC_01.004 .001")
@allure.link("https://github.com/RedRoverSchool/JenkinsQA_Python_2026_fall/issues/92")
def test_item_types_are_available(browser):
    browser.find_element(*NewItemPageLocator.ADD_NEW_ITEM).click()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(NewItemPageLocator.PIPELINE))
    pipeline = browser.find_element(*NewItemPageLocator.PIPELINE)
    pipeline.click()

    freestyle_project = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.FREESTYLE_PROJECT))
    freestyle_project.click()
    multi_config_project = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.MULTI_CONFIGURATION_PROJECT))
    multi_config_project.click()

    folder = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NewItemPageLocator.FOLDER))
    folder.click()

    multibranch = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.MULTIBRANCH_PIPELINE))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", multibranch)
    multibranch.click()

    organization_folder = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.ORGANIZATION_FOLDER))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", organization_folder)
    organization_folder.click()

    assert pipeline.is_displayed()
    assert freestyle_project.is_displayed()
    assert multi_config_project.is_displayed()
    assert folder.is_displayed()
    assert multibranch.is_displayed()
    assert organization_folder.is_displayed()


@allure.description_html("Automated by: <strong>Konstantin Kurilo</strong>")
@allure.title("TC_01.004.002 | Verify entering a valid and unique item name and creating the item")
@allure.link("https://github.com/RedRoverSchool/JenkinsQA_Python_2026_fall/issues/93")
def test_create_item_with_unique_name(browser, cleanup_item):
    browser.find_element(*NewItemPageLocator.ADD_NEW_ITEM).click()

    item_name_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(NewItemPageLocator.ITEM_NAME_INPUT))
    item_name_field.send_keys(UNIQUE_ITEM_NAME)
    error_message = browser.find_elements(*NewItemPageLocator.ERROR_MESSAGE)
    assert item_name_field.get_attribute("value") == UNIQUE_ITEM_NAME
    assert len(error_message) == 0 or not error_message[0].is_displayed()

    organization_folder = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.ORGANIZATION_FOLDER))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", organization_folder)
    organization_folder.click()

    ok_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(NewItemPageLocator.OK_BUTTON))
    ok_button.click()

    WebDriverWait(browser, 10).until(EC.url_contains("/configure"))
    assert "/configure" in browser.current_url

    jenkins_logo = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(NewItemPageLocator.JENKINS_LOGO))
    jenkins_logo.click()

    created_item = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f'//span[normalize-space()="{UNIQUE_ITEM_NAME}"]')))
    assert created_item.is_displayed()


@pytest.fixture
def cleanup_item(browser):
    """A fixture for automatically deleting a created element"""
    yield UNIQUE_ITEM_NAME

    try:
        browser.get("http://localhost:8080/")
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located(MainPageLocator.ITEM_NAME_ROW))

        dropdown_options = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(MainPageLocator.DROPDOWN_OPTIONS))
        dropdown_options.click()

        delete_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(MainPageLocator.DELETE_BUTTON))
        delete_button.click()

        yes_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(MainPageLocator.YES_BUTTON))
        yes_button.click()

        WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located(MainPageLocator.CREATED_ITEM_ROW))
    except Exception as e:
        print(f"The test element could not be deleted automatically: {e}")
