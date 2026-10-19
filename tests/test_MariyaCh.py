import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

BASE_URL = "https://shawarma.threadqa.ru"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
USERNAME = "owner"
PASSWORD = "owner123"


# ====================================================== Фикстуры =====================================================

# Открытие пустого хрома без токена для тестов стр авторизации
@pytest.fixture
def driver_no_token():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    yield driver
    driver.quit()

# Один раз перед прогоном запрашиваю токен, он хранится все время этого прогона
@pytest.fixture(scope="session")
def api_token():
    request = requests.post(
        LOGIN_URL,
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10
    )
    request.raise_for_status()
    data = request.json()
    assert "token" in data, f"Нет токена в ответе: {data}"
    return data["token"]

# Перед каждым тестом запускаю новый хром и использую уже полученный токен
@pytest.fixture
def driver(api_token):
    driver = webdriver.Chrome()

    driver.get(BASE_URL)
    driver.execute_script(
        "window.localStorage.setItem('token', arguments[0]);",
        api_token
    )
    driver.refresh()

    yield driver
    driver.quit()


# ======================================================= Тесты =======================================================

# ----------------------------------------------- Страница авторизации ------------------------------------------------

def do_login(driver_no_token, login, password):
    login_input = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-username"]')))
    password_input = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-password"]')))
    submit_button = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-submit"]')))

    login_input.send_keys(login)
    password_input.send_keys(password)
    submit_button.click()


@pytest.mark.parametrize("login, password, expected", [
    ("owner", "owner123", True),  # валидные данные
    ("admin", "wrong", False),  # неверный пароль
    ("", "fulladmin", False),  # пустой логин
    ("admin", "", False),  # пустой пароль
    ("unknown", "admin123", False),  # несуществующий юзер
])
def test_success_log_in_open_menu_page(driver_no_token, login, password, expected):
    """Проверяет, что успешно авторизованный пользователь перенаправляется на страницу с меню."""
    driver_no_token.get(f"{BASE_URL}/login")
    do_login(driver_no_token, login, password)

    try:
        WebDriverWait(driver_no_token, 10).until(EC.url_contains("/menu"))
        result = True
    except TimeoutException:
        result = False

    assert result == expected, "Пользователь не перенаправлен в /menu"


@pytest.mark.parametrize("login, password, expected", [
    ("owner", "wrong", "error"),  # неверный пароль - ошибка
    ("", "owner123", "warning"),  # пустой логин - подсказка
    ("owner", "", "warning"),  # пустой пароль - подсказка
    ("unknown", "admin123", "error"),  # несуществующий юзер - ошибка
])
def test_invalid_log_in_show_error(driver_no_token, login, password, expected):
    """Проверяет, что при неудачной авторизации пользователь видит ошибку или подсказку"""
    driver_no_token.get(f"{BASE_URL}/login")
    do_login(driver_no_token, login, password)

    if expected == "error":
        try:
            WebDriverWait(driver_no_token, 10).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, '[role="status"]'), "Invalid username or password"
                )
            )
            result = "error"
        except TimeoutException:
            result = ""

        assert result == expected, "Не появилось уведомление об ошибке после неудачной авторизации"

    if expected == "warning":
        login_input = WebDriverWait(driver_no_token, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-username"]')))
        password_input = WebDriverWait(driver_no_token, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-password"]')))
        validation_message_login = login_input.get_attribute("validationMessage")
        validation_message_password = password_input.get_attribute("validationMessage")

        assert validation_message_login or validation_message_password == "Заполните это поле.", "Не появилась подсказка об обязательном поле"

    # try:
    #     WebDriverWait(driver_no_token, 3).until(EC.url_contains("/login"))
    #     result = True
    # except TimeoutException:
    #     result = False
    #
    # assert result == expected, "Пользователь не остался на странице /login после неудачной авторизации"


# ----------------------------------------------- Главная страница ------------------------------------------------

@pytest.mark.parametrize("tabs", [
    ["menu", "orders", "stock", "stack", "events", "docs"]
])
def test_menu_page_has_all_navigation_tabs(driver, tabs):
    """Проверяет, что на главной странице отображаются все элементы навигации."""
    driver.get(f"{BASE_URL}/menu")
    tabs = ["menu", "orders", "stock", "stack", "events", "docs"]
    try:
        WebDriverWait(driver, 10).until(
            lambda d: all(d.find_elements(By.CSS_SELECTOR, f"[data-testid=\"nav-{tab}\"]") for tab in tabs)
        )
    except TimeoutException:
        pytest.fail("На странице отображаются не все элементы навигации из списка")