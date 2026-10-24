from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_search_bar() :
    driver = webdriver.Chrome()
    try:
        driver.get("https://python.org")
        print(driver.title)
        assert "Python" in driver.title

        search_bar = driver.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys("getting started with python")
        search_bar.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.url_contains("search"))
        print(driver.current_url)
        assert "getting+started+with+python" in driver.current_url
    finally:
        driver.quit()
