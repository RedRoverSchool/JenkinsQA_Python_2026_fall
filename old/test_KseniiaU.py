from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_find_menu_element():

    driver.get("https://www.labirint.ru/")

    driver.find_elements("class name", "b-header-b-menu-e-text")[2].click()

    url = driver.current_url

    assert url == "https://www.labirint.ru/best/"

    driver.quit()