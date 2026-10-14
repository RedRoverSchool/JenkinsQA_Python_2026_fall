from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_checkbox():
    driver = webdriver.Chrome()
    driver.get("https://demoqa.com/checkbox")

    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".rc-tree-switcher")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".rc-tree-treenode:nth-child(2) .rc-tree-checkbox")
    )).click()

    text = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#result")
    )).text.lower()

    assert "desktop" in text
    assert "notes" in text
    assert "commands" in text

    driver.quit()