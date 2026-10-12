from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_text_input():
    driver = webdriver.Chrome()
    driver.get("https://qapracticehub.com/?utm_source=chatgpt.com#inputs")


    text_box = driver.find_element(By.ID, "text-input")
    text_box.click()
    text_box.send_keys("Ekaterina")
    assert text_box.get_attribute("value") == "Ekaterina"
    label = driver.find_element(By.CSS_SELECTOR, '[for="text-input"]')
    assert label.text == "Text Input"
    time.sleep(5)
    driver.quit()

    #test
