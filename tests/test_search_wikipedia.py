from selenium import webdriver
from selenium.webdriver.common.by import By

def test_search_wikipedia():
    driver = webdriver.Chrome()

    driver.get("https://www.wikipedia.org/")
    driver.implicitly_wait(0.5)

    search_area = driver.find_element(by=By.NAME, value="search")
    search_button = driver.find_element(by=By.CSS_SELECTOR, value=".pure-button.pure-button-primary-progressive")

    search_area.send_keys("Selenium")
    search_button.click()

    driver_title = driver.find_element(by=By.CSS_SELECTOR, value=".mw-page-title-main")
    assert driver_title.text == "Selenium"

    driver.quit()