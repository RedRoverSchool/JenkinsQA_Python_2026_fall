from selenium.webdriver.common.by import By

def test_open_manage_jenkins(browser):
    manage_button = browser.find_element(By.ID, "root-action-ManageJenkinsAction")
    manage_button.click()

    manage_heading = browser.find_element(By.CSS_SELECTOR, "#main-panel > div > div.jenkins-app-bar__content > h1")

    assert manage_heading.text == "Manage Jenkins"