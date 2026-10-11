from selenium import webdriver
from selenium.webdriver.common.by import By

def test_open_page():
    driver = webdriver.Chrome()
    driver.get("https://automationteststore.com/")
    driver.implicitly_wait(10)

    button = driver.find_element(By.XPATH, "//*[@id='categorymenu']/nav/ul/li[8]/a")
    button.click()
    driver.implicitly_wait(5)

    assert driver.current_url == "https://automationteststore.com/index.php?rt=product/category&path=65"

    driver.quit()