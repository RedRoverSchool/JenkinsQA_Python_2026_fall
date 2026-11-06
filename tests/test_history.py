import os
import re
from collections import Counter
from datetime import datetime

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BUILD_HISTORY_URL = os.getenv(
    "JENKINS_BUILD_HISTORY_URL",
    "http://localhost:8080/view/all/builds",
)

TABLE = (By.ID, "projectStatus")
TIMEOUT = 15


@pytest.fixture
def history(driver):
    driver.get(BUILD_HISTORY_URL)

    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.visibility_of_element_located(TABLE))
    wait.until(
        lambda browser: len(
            browser.find_elements(
                By.CSS_SELECTOR, "#projectStatus tbody tr"
            )
        ) >= 2,
        message="Для проверки нужны минимум две сборки",
    )

    return driver


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
        cell = row.find_elements(By.TAG_NAME, "td")[column_index]

        if column_index == 0:

            value = int(cell.get_dom_attribute("data"))

        elif column_index == 2:

            value = datetime.fromisoformat(
                cell.get_dom_attribute("data").replace("Z", "+00:00")
            )

        else:

            text = cell.get_attribute("textContent")
            value = re.sub(r"\s+", " ", text).strip().casefold()

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
def test_each_column_supports_sorting(history, column_index):
    driver = history
    wait = WebDriverWait(driver, TIMEOUT)

    headers = driver.find_elements(
        By.CSS_SELECTOR, "#projectStatus thead th"
    )
    header = headers[column_index]

    assert header.get_dom_attribute("data-sort-disable") != "true"

    sort_link = header.find_element(
        By.CSS_SELECTOR, "a.sortheader"
    )
    assert sort_link.is_displayed()
    assert sort_link.is_enabled()

    before_ids = Counter(build_ids(driver))
    before_values = column_values(driver, column_index)

    if len(set(before_values)) < 2:
        pytest.skip(
            "У всех сборок одинаковые значения колонки. "
            "Нужны минимум два различных значения."
        )

    sort_link.click()

    wait.until(
        lambda _: header.find_element(
            By.CSS_SELECTOR, ".sortarrow"
        ).get_attribute("textContent").strip(),
        message="У выбранной колонки не появился индикатор сортировки",
    )

    wait.until(
        lambda browser: is_sorted(
            column_values(browser, column_index)
        ),
        message="Значения выбранной колонки не упорядочены",
    )

    assert Counter(build_ids(driver)) == before_ids, (
        "После сортировки изменился состав сборок"
    )


def test_console_output_header_does_not_sort(history):
    driver = history

    headers = driver.find_elements(
        By.CSS_SELECTOR, "#projectStatus thead th"
    )
    console_header = headers[-1]

    assert console_header.get_dom_attribute(
        "data-sort-disable"
    ) == "true"
    assert not console_header.find_elements(
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

    assert build_ids(driver) == before_ids, (
        "Console Output изменил порядок сборок"
    )

    after_arrows = [
        element.get_attribute("textContent")
        for element in driver.find_elements(
            By.CSS_SELECTOR, "#projectStatus .sortarrow"
        )
    ]

    assert after_arrows == before_arrows, (
        "Console Output изменил текущую сортировку"
    )
    assert driver.current_url == before_url