import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NAME = "QA Laras"


def test_book_demo_and_submit_contact_form(driver):
    wait = WebDriverWait(driver, 15)
    driver.maximize_window()

    driver.get("https://www.5days.com/")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//main//a[contains(., 'Book a demo')]"))).click()
    wait.until(EC.url_contains("/contact"))

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='tally.so']")))

    time.sleep(1)


    name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter your full name']")))
    name.send_keys(NAME)
    #wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input[placeholder='Enter your full name']"), NAME))

    email = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email address']")
    email.send_keys("qa.test@example.com")

    driver.find_element(By.CSS_SELECTOR, "input[role='combobox']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@role='option'][contains(., 'Ask a demo')]"))).click()

    driver.find_element(By.TAG_NAME, "textarea").send_keys("Please ignore.")

    # Submit and check the form goes away
    submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
    driver.execute_script("arguments[0].click();", submit)
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(., 'Submit')]")))