import string
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def test_successful_creating(browser):
    name_pipeline = ''.join(random.choices(string.ascii_lowercase, k=10))

    create_item_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class = 'task-link-text' and contains(text(), 'Item')]/.."))
    )
    create_item_button.click()

    field_name = browser.find_element(By.ID, "name")
    field_name.send_keys({name_pipeline})

    pipeline_button = browser.find_element(By.XPATH, "//span[text() = 'Pipeline']")
    pipeline_button.click()

    ok_button = browser.find_element(By.ID, "ok-button")
    ok_button.click()

    save_button = browser.find_element(By.XPATH, "//button[@value = 'Save']")
    save_button.click()

    assert WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[normalize-space(.) = '{name_pipeline}']"))
    )

