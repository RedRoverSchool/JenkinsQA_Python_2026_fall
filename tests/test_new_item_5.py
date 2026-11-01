from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def test_cannot_create_item_with_empty_name(browser):
    wait = WebDriverWait(
        browser,
        10,
        ignored_exceptions=(StaleElementReferenceException,)
    )

    new_item_link = (By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    name_field = (By.ID, "name")
    folder_type = (
        By.CSS_SELECTOR,
        "input[value='com.cloudbees.hudson.plugins.folder.Folder'] + span"
    )
    ok_button = (By.ID, "ok-button")

    wait.until(
        EC.element_to_be_clickable(new_item_link)
    ).click()

    wait.until(EC.url_contains("/view/all/newJob"))

    assert wait.until(
        lambda driver: driver.find_element(*name_field).is_displayed()
    )

    assert wait.until(
        lambda driver: (
            driver.find_element(*name_field).get_attribute("value") == ""
        )
    )

    wait.until(
        EC.element_to_be_clickable(folder_type)
    ).click()

    assert wait.until(
        lambda driver: not driver.find_element(*ok_button).is_enabled()
    )