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


def test_login():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Login-Portal/index.html")

    username = driver.find_element(By.ID, "text")
    username.send_keys("webdriver")

    password = driver.find_element(By.ID, "password")
    password.send_keys("webdriver123")

    login_button = driver.find_element(By.CSS_SELECTOR, "#login-button")
    login_button.click()

    alert = driver.switch_to.alert
    alert_text = alert.text

    assert alert_text == "validation succeeded"

    alert.accept()

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


def test_button_click():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Click-Buttons/index.html")

    button = driver.find_element(By.ID, "button1")
    button.click()
    time.sleep(1)
    assert button.is_enabled() == True

    message = driver.find_element(
        By.CSS_SELECTOR,
        "div[id='myModalClick'] h4[class='modal-title']"  )

    text = message.text

    assert text == "Congratulations!"

    close_button = driver.find_element( By.CSS_SELECTOR,
        "div[id='myModalClick'] div[class='modal-footer'] button[type='button']" )
    close_button.click()

    driver.quit()


def test_double_click():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Actions/index.html")

    double_click = driver.find_element(By.ID, "double-click")
    ActionChains(driver).double_click(double_click).perform()
    background_color = double_click.value_of_css_property("background-color")

    assert background_color == "rgba(31, 31, 31, 1)"

    driver.quit()


def test_drag_and_drop():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Actions/index.html")

    draggable = driver.find_element(By.ID, "draggable")
    droppable = driver.find_element(By.ID, "droppable")
    ActionChains(driver).drag_and_drop(draggable, droppable).perform()
    result = droppable.text

    assert result == "Dropped!"

    driver.quit()


def test_click_and_hold():
    driver = webdriver.Chrome()

    driver.get("https://webdriveruniversity.com/Actions/index.html")

    click_box = driver.find_element(By.ID, "click-box")

    ActionChains(driver).click_and_hold(click_box).perform()

    assert click_box.text == "Well done! keep holding that click now....."

    ActionChains(driver).release().perform()

    driver.quit()