import re
from collections import Counter
from datetime import datetime

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.project_utils import get_url


BUILD_HISTORY_URL = f"{get_url().rstrip('/')}/view/all/builds"

TABLE = (By.ID, "projectStatus")


@pytest.fixture(scope="function")
def wait10(browser):
    return WebDriverWait(browser, timeout=10)


@pytest.fixture
def history(browser, wait10):
    try:
        wait10.until(
            lambda driver: (
                "/login" not in driver.current_url
                and not driver.find_elements(
                    By.NAME, "j_username"
                )
            ),
            message="Авторизация Jenkins не завершена",
        )
    except TimeoutException:
        pytest.fail(
            "Не удалось авторизоваться в Jenkins. "
            "Проверь JENKINS_USERNAME и JENKINS_PASSWORD в .env. "
            f"Текущий URL: {browser.current_url}"
        )

    browser.get(BUILD_HISTORY_URL)

    if browser.find_elements(By.NAME, "j_username"):
        pytest.fail(
            "Jenkins повторно перенаправил на страницу входа. "
            f"Текущий URL: {browser.current_url}"
        )

    wait10.until(
        EC.visibility_of_element_located(TABLE),
        message="Таблица Build History не найдена",
    )

    return browser


def rows(driver):
    return driver.find_elements(
        By.CSS_SELECTOR, "#projectStatus tbody tr"
    )


def build_ids(driver):
    return [
        row.find_element(
            By.CSS_SELECTOR, "a.jenkins-badge"
        ).get_attribute("href")
        for row in rows(driver)
    ]


def column_values(driver, column_index):
    values = []

    for row in rows(driver):
        cell = row.find_elements(
            By.TAG_NAME, "td"
        )[column_index]

        if column_index == 0:

            value = int(
                cell.get_dom_attribute("data")
            )

        elif column_index == 2:

            value = datetime.fromisoformat(
                cell.get_dom_attribute("data").replace(
                    "Z", "+00:00"
                )
            )

        else:

            text = cell.get_attribute("textContent")
            value = re.sub(
                r"\s+", " ", text
            ).strip().casefold()

        values.append(value)

    return values


def is_sorted(values):
    return (
        values == sorted(values)
        or values == sorted(values, reverse=True)
    )


@pytest.mark.parametrize(
    "column_index",
    [
        pytest.param(0, id="S"),
        pytest.param(1, id="Build"),
        pytest.param(2, id="Time-Since"),
        pytest.param(3, id="Status"),
    ],
)
def test_each_column_supports_sorting(
    history, wait10, column_index
):
    driver = history

    if len(rows(driver)) < 2:
        pytest.skip(
            "Недостаточно сборок для проверки сортировки. "
            "Необходимы минимум две сборки."
        )

    headers = driver.find_elements(
        By.CSS_SELECTOR, "#projectStatus thead th"
    )
    header = headers[column_index]

    sort_disabled = header.get_dom_attribute(
        "data-sort-disable"
    )

    sort_link = header.find_element(
        By.CSS_SELECTOR, "a.sortheader"
    )

    is_visible = sort_link.is_displayed()
    is_enabled = sort_link.is_enabled()

    before_ids = Counter(build_ids(driver))
    before_values = column_values(
        driver, column_index
    )

    if len(set(before_values)) < 2:
        pytest.skip(
            "У всех сборок одинаковые значения колонки. "
            "Нужны минимум два различных значения."
        )

    sort_link.click()

    wait10.until(
        lambda _: header.find_element(
            By.CSS_SELECTOR, ".sortarrow"
        ).get_attribute("textContent").strip(),
        message=(
            "У выбранной колонки не появился "
            "индикатор сортировки"
        ),
    )

    wait10.until(
        lambda browser: is_sorted(
            column_values(browser, column_index)
        ),
        message=(
            "Значения выбранной колонки "
            "не упорядочены"
        ),
    )

    after_ids = Counter(build_ids(driver))

    assert sort_disabled != "true"
    assert is_visible
    assert is_enabled
    assert after_ids == before_ids, (
        "После сортировки изменился состав сборок"
    )


def test_console_output_header_does_not_sort(history):
    driver = history

    headers = driver.find_elements(
        By.CSS_SELECTOR, "#projectStatus thead th"
    )
    console_header = headers[-1]

    sort_disabled = console_header.get_dom_attribute(
        "data-sort-disable"
    )

    sort_links = console_header.find_elements(
        By.CSS_SELECTOR, "a.sortheader"
    )

    before_ids = build_ids(driver)

    before_arrows = [
        element.get_attribute("textContent")
        for element in driver.find_elements(
            By.CSS_SELECTOR, "#projectStatus .sortarrow"
        )
    ]

    before_url = driver.current_url

    console_header.click()

    after_ids = build_ids(driver)

    after_arrows = [
        element.get_attribute("textContent")
        for element in driver.find_elements(
            By.CSS_SELECTOR, "#projectStatus .sortarrow"
        )
    ]

    after_url = driver.current_url

    assert sort_disabled == "true"
    assert not sort_links
    assert after_ids == before_ids, (
        "Console Output изменил порядок сборок"
    )
    assert after_arrows == before_arrows, (
        "Console Output изменил текущую сортировку"
    )
    assert after_url == before_url
