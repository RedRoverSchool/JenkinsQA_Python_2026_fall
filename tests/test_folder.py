from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_folder_from_dashboard(browser):
    """TC_01.002.01 | Verify successful creation of a Folder from the Dashboard"""

    folder_name = "TestFolder_01"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()

    browser.find_element(By.ID, "name").send_keys(folder_name)

    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()

    browser.find_element(By.ID, "ok-button").click()

    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )

    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, timeout=10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), folder_name)
    )

    assert folder_name in browser.find_element(By.TAG_NAME, "h1").text