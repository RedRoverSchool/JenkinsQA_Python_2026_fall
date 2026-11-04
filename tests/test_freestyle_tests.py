from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def test_freestyle_tests(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()

    item_name = "Freestyle Project 1"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[value='Save']")))
    save_button = browser.find_element(By.CSS_SELECTOR, "[value='Save']")
    save_button.click()

    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),item_name))

    assert item_name in browser.find_element(By.TAG_NAME, "h1").text

def test_exetute_windows_step(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item = browser.find_element(By.CSS_SELECTOR, "a[href='/view/all/newJob']")
    new_item.click()

    item_name = "Freestyle Project with Execute Windows step"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/span/button')))
    add_build_steps = browser.find_element(By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/span/button')
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_build_steps)
    add_build_steps.click()

    execute_windows_dropdown = browser.find_element(By.XPATH, '//*[@id="tippy-5"]/div/div/div/div[2]/button[1]')
    execute_windows_dropdown.click()

    command_test = "Test Command"
    command_text = browser.find_element(By.CSS_SELECTOR, "[name='command']")
    command_text.send_keys(command_test)

    advanced_button = browser.find_element(By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div/div[4]/div[2]/div[1]/button')
    advanced_button.click()

    error_test = '111'
    error_level_field = browser.find_element(By.CSS_SELECTOR, '[min="-2147483648"]')
    error_level_field.send_keys(error_test)

    add_env_filter = browser.find_element(By.XPATH, '//button[@suffix="configuredLocalRules"]')
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_env_filter)
    add_env_filter.click()

    keep_specified = browser.find_element(By.XPATH, '//button[contains(text(), "Keep Specified Environment")]')
    keep_specified.click()

    variable_test = '222'
    variables_field = browser.find_element(By.CSS_SELECTOR, "[name='_.variables']")
    variables_field.send_keys(variable_test)

    submit_button = browser.find_element(By.CSS_SELECTOR, "[name='Submit']")
    submit_button.click()

    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), item_name))
    assert item_name in browser.find_element(By.TAG_NAME, "h1").text


