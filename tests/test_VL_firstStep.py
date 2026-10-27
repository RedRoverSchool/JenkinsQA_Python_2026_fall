from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_welcome_to_jenkins(browser):
    label = browser.find_element(By.CSS_SELECTOR, "div.empty-state-block > h1")
    assert label.text == "Welcome to Jenkins!"


def test_history_of_buildings(browser):
    wait = WebDriverWait(browser, 10)
    history_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Build History"))
    )
    history_link.click()

    heading = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main-panel"]/div[1]/div/h1')
        )
    )
    assert heading.text.__contains__("Build History")



