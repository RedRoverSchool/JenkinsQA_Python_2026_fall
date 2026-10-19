from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Вспомогательная функция
def run_form_submit(first_name, last_name):
    url = "https://ultimateqa.com/sample-application-lifecycle-sprint-2/"
    driver = webdriver.Chrome()
    try:
        driver.get(url)

        # Даём странице загрузиться
        time.sleep(2)

        # Находим поля и кнопку по CSS-селекторам
        input_first = driver.find_element(By.CSS_SELECTOR, "input[name='firstname']")
        input_last = driver.find_element(By.CSS_SELECTOR, "input[name='lastname']")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        # Вводим данные
        input_first.send_keys(first_name)
        input_last.send_keys(last_name)

        # Нажимаем кнопку
        submit_btn.click()

        # Ждём, пока откроется новая страница и загрузится контент
        time.sleep(3)

        # Проверяем, что мы действительно на новой странице
        assert "home.ultimateqa.com" in driver.current_url, "Ожидался редирект на home.ultimateqa.com, но URL другой."
    finally:
        # Закрываем браузер после каждого запуска, даже при ошибке
        driver.quit()

# Тесты для pytest
def test_anna_petrova():
    run_form_submit("Анна", "Петрова")

def test_ivan_ivanov():
    run_form_submit("Иван", "Иванов")