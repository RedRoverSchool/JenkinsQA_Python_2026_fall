import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_website():
    driver = webdriver.Chrome()

    driver.get("https://belpost.by/")

    title = driver.title

    time.sleep(5)

    text_box = driver.find_element(by=By.NAME, value="number")
    submit_button = driver.find_element(by=By.XPATH, value="//*[@id=\"shell-content\"]/app-pages/app-home/main/section[2]/div/app-base-widget/section/div/div/form/label/div/button")

    text_box.send_keys("BY123456789BY")
    time.sleep(5)

    submit_button.click()

    time.sleep(5)

