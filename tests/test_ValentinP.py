import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def test_radio_buttons():
    driver = webdriver.Chrome()

    driver.get("https://ultimateqa.com/simple-html-elements-for-automation/")

    male = driver.find_element(By.CSS_SELECTOR, "input[value='male']")
    female = driver.find_element(By.CSS_SELECTOR, "input[value='female']")
    driver.execute_script("arguments[0].click();", male)
    assert male.is_selected()

    driver.execute_script("arguments[0].click();", female)
    assert female.is_selected()
    assert not male.is_selected()

    driver.quit()


def test_contact_us():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Contact-Us/contactus.html")

    first_name = driver.find_element(By.NAME, "first_name")
    first_name.send_keys("Valentin")

    last_name = driver.find_element(By.NAME, "last_name")
    last_name.send_keys("Podkova")

    email = driver.find_element(By.NAME, "email")
    email.send_keys("valentin@test.com")

    message = driver.find_element(By.NAME, "message")
    message.send_keys("This is a test message")

    button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    button.click()

    success_message = driver.find_element(By.TAG_NAME, "h1")

    assert success_message.text == "Thank You for your Message!"

    driver.quit()


def test_dropdowm():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")

    dropdown = driver.find_element(By.ID, "dropdowm-menu-1")
    select = Select(dropdown)
    select.select_by_visible_text("JAVA")

    selected_option = select.first_selected_option
    assert selected_option.text == "JAVA"

    driver.quit()