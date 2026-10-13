from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_current_date():

    driver = webdriver.Chrome()

    driver.get("https://today-date.com/")
    driver.implicitly_wait(0.5)

    title = driver.title

    current_date = driver.find_element(by=By.ID, value="td-main-date")
    page_date_text = current_date.text

    current_system_date = datetime.now().strftime("%m/%d/%Y")

    assert page_date_text == current_system_date, f"Ожидалось {current_system_date}, но на странице {page_date_text}"

    driver.quit()
