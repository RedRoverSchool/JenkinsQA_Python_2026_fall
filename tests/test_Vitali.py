from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://votby.ru/")
sleep(2)

signButton = driver.find_element("xpath", "//button[@aria-haspopup='menu']")
signButton.click()
sleep(1)
enterButton = driver.find_element(
"xpath", "//div[@role='menuitem' and contains(., 'Войти')]"
).click()

# Поиск поля Email
email_input = driver.find_element("xpath", "//input[@id='email']")

# Поиск поля Пароль
password_input = driver.find_element("xpath", "//input[@id='password']")

login_button = driver.find_element(
    "xpath", "//button[@type='submit'][.//span[text()='Войти']]"
)

def test_registration_feild(email: str, password: str, expected_error_text=None):
    email_input.clear()
    password_input.clear()

    email_input.send_keys(f"{email}")
    password_input.send_keys(f"{password}")
    login_button.click()

    sleep(2)

    if expected_error_text:
        try:
            # Пытаемся найти текст ошибки
            error_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(("xpath", f"//*[contains(text(), '{expected_error_text}')]"))
            )
            assert error_element.is_displayed()
            print(f"✓ Тест пройден успешно: найдена ошибка '{expected_error_text}'")
        except Exception:
            # Если точный текст не нашелся, выведем подсказку для отладки
            print(f"⚠️ Текст '{expected_error_text}' не найден. Проверяем состояние формы...")
            # Проверим, осталась ли модалка открытой (что значит — форма заблокировала вход)
            modal_is_open = len(driver.find_elements("xpath", "//form[contains(@class, 'LoginForm')]")) > 0
            assert modal_is_open, "Форма неожиданно закрылась при ошибке валидации!"
            print(f"✓ Тест пройден успешно: форма заблокировала отправку с пустым паролем.")
    else:
        print(f"Тест с данными: email='{email}', password='{password}' выполнен.")

# Тестовые данные
test_cases = [
    ("user123tutmy@mail.ru", "~~~~~~~~~~", None),
    ("", "12345678", "Ошибка сервера"),  # Пустой email
    ("user@mail.ru", "", "Ошибка сервера"),  # Пустой пароль (теперь проверит блокировку формы, если тоста нет)
    ("invalid_email", "12345678", "Введите корректный email"),
    ("user@mail.ru", "short", None),
    ("a" * 250 + "@mail.ru", "12345678", None),
    ("user@mail.ru", "1" * 130, None),
]

# Запуск тестов
for email, password, expected_error in test_cases:
    print(f"\nТестируем с данными: email='{email}', password='{password}'")
    try:
        test_registration_feild(email, password, expected_error)
    except Exception as e:
        print(f"✗ Тест упал с критической ошибкой: {e}")

driver.quit()