import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_create_folder(browser, wait5):

    folder_name = "mark-georg"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(folder_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )
    browser.find_element(By.NAME, "Submit").click()

    wait5.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), folder_name)
    )

    assert folder_name in browser.find_element(By.TAG_NAME, "h1").text


def test_create_two_folder(browser, wait5):

    first_name = "mark-georg"
    two_name = "mark"

    browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']").click()
    browser.find_element(By.ID, "name").send_keys(first_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )
    browser.find_element(By.NAME, "Submit").click()

    wait5.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), first_name)
    )
    browser.find_element(By.XPATH, "//a[contains(@href, 'newJob')]").click()

    browser.find_element(By.ID, "name").send_keys(two_name)
    browser.find_element(By.XPATH, "//span[normalize-space()='Folder']").click()
    browser.find_element(By.ID, "ok-button").click()

    wait5.until(
        EC.visibility_of_element_located((By.NAME, "Submit"))
    )
    browser.find_element(By.NAME, "Submit").click()

    wait5.until(
        EC.presence_of_element_located((By.CLASS_NAME, "jenkins-breadcrumbs__list"))
    )
    breadcrumbs_text = browser.find_element(By.CLASS_NAME, "jenkins-breadcrumbs__list").text

    assert first_name in breadcrumbs_text
    assert two_name in breadcrumbs_text
