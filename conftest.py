import logging
from selenium.webdriver.chrome.options import Options
import pytest
from selenium import webdriver


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WebDriver")

@pytest.fixture(scope="function")
def driver(chrome_options):
    logger.info("Starting Chrome browser session...")
    driver = webdriver.Chrome(options=chrome_options)
    logger.info("Closing Chrome browser session...")
    yield driver
    driver.quit()

@pytest.fixture
def chrome_options():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-cache")
    options.add_argument('--start-maximized')
    return options


