from selenium.webdriver.common.by import By
import time

def test_create_new_folder(browser):
    browser.find_element(By. LINK_TEXT, "New Item").click()

    browser.find_element(By.ID, "name").send_keys("Project_1")

    browser.find_element(By. XPATH, "//*[@id='items']/div[4]/label/span").click()

    browser.find_element(By.ID, "ok-button").click()

    time.sleep(2)

    browser.find_element(By. NAME, "_.displayNameOrNull").send_keys("First Job")
    browser.find_element(By. CSS_SELECTOR, "#bottom-sticker > div > button.jenkins-button.jenkins-submit-button.jenkins-button--primary").click()
    time.sleep(2)

    assert browser.find_element(By. XPATH, "//*[@id='main-panel']/div[1]/div/h1").text == "First Job"
