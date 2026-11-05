import pytest
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from common.filter_utils import filter_items_by_changed_files
from common.jenkins_utils import login, logout, clear_data
from common.order_utils import reorder_items_by_dependency
from common.project_utils import get_browser, get_options, get_url


@pytest.fixture(scope="function")
def browser(request):
    get_browser()

    dependency_marker = request.node.get_closest_marker("dependency")
    depends = dependency_marker.kwargs.get("depends") if dependency_marker else None
    if not depends:
        print("\nclearing data")
        clear_data()

    options = webdriver.ChromeOptions()
    for option in get_options():
        options.add_argument(option)
    print("opening browser")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6)

    print("getting page")
    driver.get(get_url())
    login(driver)
    try:
        yield driver
    finally:
        try:
            logout(driver)
        finally:
            driver.quit()


@pytest.fixture(scope="function")
def wait2(browser):
    return WebDriverWait(browser, 2)


@pytest.fixture(scope="function")
def wait5(browser):
    return WebDriverWait(browser, 5)


@pytest.fixture(scope="function")
def wait10(browser):
    return WebDriverWait(browser, 10)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "dependency(name=None, depends=None): dependencies between tests",
    )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(session, config, items):
    items[:] = filter_items_by_changed_files(items)
    reorder_items_by_dependency(items)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "browser" in item.fixturenames:
                web_driver = item.funcargs["browser"]

                folder_name = "screenshots"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                clean_test_name = item.name.replace('[', '_').replace(']', '_').replace(':', '_')
                screenshot_path = os.path.join(folder_name, f"failed_{clean_test_name}.png")

                web_driver.save_screenshot(screenshot_path)
                print(f"\n[Скриншот ошибки успешно сохранен: {screenshot_path}]")
        except Exception as e:
            print(f"\nНе удалось создать скриншот при падении: {e}")