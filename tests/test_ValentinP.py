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


def test_checkbox():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")

    checkbox = driver.find_element(By.CSS_SELECTOR, "input[value='option-1']")

    assert checkbox.is_selected() == False
    checkbox.click()
    assert checkbox.is_selected() == True

    checkbox3 = driver.find_element(By.CSS_SELECTOR, "input[value='option-3']")
    assert checkbox3.is_selected() == True

    driver.quit()


def test_radio_button():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")

    radio = driver.find_element(By.CSS_SELECTOR, "input[value='green']")

    radio.click()

    assert radio.is_selected() == True

    radio_blue = driver.find_element(By.CSS_SELECTOR, "input[value='blue']")

    radio_blue.click()

    assert radio_blue.is_selected() == True
    assert radio.is_selected() == False

    driver.quit()


def test_second_dropdown():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")

    dropdown = driver.find_element(By.ID, "dropdowm-menu-2")
    select = Select(dropdown)

    select.select_by_visible_text("Eclipse")

    assert select.first_selected_option.text == "Eclipse"

    driver.quit()


def test_disabled_radio_button():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Dropdown-Checkboxes-RadioButtons/index.html")

    cabbage = driver.find_element(By.CSS_SELECTOR, "input[value='cabbage']")

    assert cabbage.is_enabled() == False

    pumpkin = driver.find_element(By.CSS_SELECTOR, "input[value='pumpkin']")

    assert pumpkin.is_selected() == True

    fruit_dropdown = driver.find_element(By.ID, "fruit-selects")
    fruit_select = Select(fruit_dropdown)

    assert fruit_select.first_selected_option.text == "Grape"

    orange = driver.find_element(
        By.CSS_SELECTOR, "#fruit-selects option[value='orange']"
    )

    assert orange.is_enabled() == False

    driver.quit()