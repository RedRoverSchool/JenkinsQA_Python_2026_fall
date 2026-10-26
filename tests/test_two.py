from selenium import webdriver
from selenium.webdriver.common.by import By


def test_two():
    driver = webdriver.Chrome()
    driver.get("https://belmeta.com/?ysclid=mv4x7jjqef759142263")
    driver.implicitly_wait(3)
    driver.maximize_window()
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    submit_button.click()
    title = driver.find_element(by=By.CSS_SELECTOR, value='h1')

    driver.quit()
