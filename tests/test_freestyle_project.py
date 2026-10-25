from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_freestyle_project(browser):
    project_name = "Python_Freestyle_Test"

    browser.find_element(
        By.CSS_SELECTOR, "a[href='/view/all/newJob']"
    ).click()

    browser.find_element(By.ID, "name").send_keys(project_name)

    browser.find_element(
        By.XPATH, "//span[normalize-space()='Freestyle project']/parent::label"
    ).click()

    browser.find_element(By.ID, "ok-button").submit()

    WebDriverWait(browser, 10).until(
        EC.url_contains(f"/job/{project_name}/")
    )

    assert project_name in browser.find_element(By.TAG_NAME, "body").text
    assert "Configure" in browser.find_element(By.TAG_NAME, "body").text

    browser.find_element(By.NAME, "Submit").click()

    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "Build Now"
        )
    )

    assert "Build Now" in browser.find_element(By.TAG_NAME, "body").text

    browser.find_element(
        By.CSS_SELECTOR,
        f"a[href='/job/{project_name}/build?delay=0sec']"
    ).click()

    assert "Builds" in browser.find_element(By.TAG_NAME, "body").text
