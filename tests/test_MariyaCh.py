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

def do_login(driver_no_token):
    login_input = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-username"]')))
    password_input = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-password"]')))
    submit_button = WebDriverWait(driver_no_token, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="login-submit"]')))

    login_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    submit_button.click()

def test_success_log_in_open_menu_page(driver_no_token):
    """Проверяет, что успешно авторизованный пользователь перенаправляется на страницу с меню."""
    driver_no_token.get(f"{BASE_URL}/login")
    do_login(driver_no_token)

    try:
        WebDriverWait(driver_no_token, 10).until(EC.url_contains("/menu"))
    except TimeoutException:
        pytest.fail("Пользователь не перенаправлен в /menu")

    try:
        WebDriverWait(driver_no_token, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="logout-btn"]'))
        )
    except TimeoutException:
        pytest.fail("Кнопка EXIT не появилась в /menu после логина")


# def test_invalid_log_in_show_error(driver_no_token):
#     """Проверяет, что при неудачной авторизации пользователь видит ошибку и остается на той же странице."""
#     driver_no_token.get(f"{BASE_URL}/login")
#     do_login(driver_no_token)
#
#     try:
#         WebDriverWait(driver_no_token, 10).until(
#             EC.text_to_be_present_in_element(
#                 (By.CSS_SELECTOR, '[role="status"]'), "Invalid username or password"
#             )
#         )
#     except TimeoutException:
#         pytest.fail("Не появилось уведомление об ошибке после неудачной авторизации")
#
#     try:
#         WebDriverWait(driver_no_token, 10).until(EC.url_contains("/login"))
#     except TimeoutException:
#         pytest.fail("Пользователь не остался на странице /login после неудачной авторизации")


# ----------------------------------------------- Главная страница ------------------------------------------------

def test_menu_page_has_all_navigation_tabs(driver):
    """Проверяет, что на главной странице отображаются все элементы навигации."""
    driver.get(f"{BASE_URL}/menu")
    tabs = ["menu", "orders", "stock", "stack", "events", "docs"]
    try:
        WebDriverWait(driver, 10).until(
            lambda d: all(d.find_elements(By.CSS_SELECTOR, f"[data-testid=\"nav-{tab}\"]") for tab in tabs)
        )
    except TimeoutException:
        pytest.fail("На странице отображаются не все элементы навигации из списка")