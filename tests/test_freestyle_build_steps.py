from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

def test_freestyle_tests(browser, wait10):
    new_item = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()

    item_name = "Freestyle Project 1"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    save_button = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[value='Save']")))
    save_button.click()

    wait10.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),item_name))

    assert item_name in browser.find_element(By.TAG_NAME, "h1").text


def test_exetute_windows_step(browser, wait10):
    new_item = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()

    item_name = "Freestyle Project with Execute Windows step"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    add_build_steps = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/span/button')))
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

    wait10.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), item_name))
    assert item_name in browser.find_element(By.TAG_NAME, "h1").text


def test_execute_shell_and_invoke_ant(browser, wait10):
    new_item = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()

    item_name = "Freestyle Project with two Build Steps"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    add_build_steps = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[suffix = 'builder']")))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_build_steps)
    add_build_steps.click()

    search_field = browser.find_element(By.XPATH, "//input[@type='search' and @placeholder='Filter']")
    execute_shell = 'Execute shell'
    search_field.send_keys(execute_shell)

    execute_shell_dropdown = browser.find_element(By.XPATH, '//*[@id="tippy-5"]/div/div/div/div[2]/button[2]')
    execute_shell_dropdown.click()

    command = 'test command'
    shell_command = browser.find_element(By.XPATH, "//div[@class='CodeMirror-scroll cm-s-default']")
    shell_command.send_keys(command)

    advanced_button = wait10.until(element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div/div[4]/div[2]/div[1]/button')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_button)
    advanced_button.click()

    error_validation = 333333333
    error_field = browser.find_element(By.CSS_SELECTOR, "[name = '_.unstableReturn']")
    error_field.send_keys(error_validation)
    browser.find_element(By.TAG_NAME, "body").click()

    error_text = 'Invalid exit code value'
    wait10.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div/div[4]/div[3]/div[1]/div[3]/div'), error_text))
    assert error_text in browser.find_element(By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div/div[4]/div[3]/div[1]/div[3]/div').text

    error_field.clear()
    error_field.send_keys(22)
    browser.find_element(By.TAG_NAME, "body").click()

    add_env_filter = browser.find_element(By.CSS_SELECTOR, "[suffix='configuredLocalRules']")
    add_env_filter.click()

    only_keep_specified = browser.find_element(By.CSS_SELECTOR, '#tippy-20>div>div>div>div.jenkins-dropdown.jenkins-dropdown--compact>button')
    only_keep_specified.click()

    variable_field = browser.find_element(By.CSS_SELECTOR, "[name='_.variables']")
    variable_field.send_keys("Test")

    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_build_steps)
    add_build_steps.click()

    invoke_ant_dropdown = browser.find_element(By.XPATH, "//div[@class='tippy-content']/div/div[2]/button[3]")
    invoke_ant_dropdown.click()

    targets_field = browser.find_element(By.CSS_SELECTOR, "[name='_.targets']")
    targets_field.send_keys("Targets test")

    invoke_advanced = wait10.until(element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div[2]/div[4]/div[2]/div[1]/button')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", invoke_advanced)
    invoke_advanced.click()

    build_file_field = browser.find_element(By.CSS_SELECTOR, "[name='_.buildFile']")
    build_file_field.send_keys("Test 1")

    properties_field = browser.find_element(By.CSS_SELECTOR, "[name='_.properties']")
    properties_field.send_keys("Test 2")

    java_options_field = browser.find_element(By.CSS_SELECTOR, "[name='_.antOpts']")
    java_options_field.send_keys("Test 3")

    save_button = browser.find_element(By.NAME, 'Submit')
    save_button.click()

    wait10.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), item_name))
    assert item_name in browser.find_element(By.TAG_NAME, "h1").text

def test_invoke_grand_script_and_set_build_status(browser, wait10):
    new_item = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/view/all/newJob']")))
    new_item.click()

    item_name = "Freestyle Project with two Build Steps"
    name_field = browser.find_element(By.CSS_SELECTOR, "input#name")
    name_field.send_keys(item_name)

    freestyle = browser.find_element(By.XPATH, "//*[text()='Freestyle project']")
    freestyle.click()

    ok_button = browser.find_element(By.CSS_SELECTOR, "button#ok-button")
    ok_button.click()

    add_build_steps = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[suffix = 'builder']")))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_build_steps)
    add_build_steps.click()

    invoke_gradle_dropdown = browser.find_element(By.XPATH, '//*[@id="tippy-5"]/div/div/div/div[2]/button[4]')
    invoke_gradle_dropdown.click()

    use_gradle_wrapper_radiobutton = browser.find_element(By.CSS_SELECTOR, '[for="radio-block-31"]')
    use_gradle_wrapper_radiobutton.click()

    make_executable_checkbox = wait10.until(element_to_be_clickable((By.XPATH, '//input[@name="_.makeExecutable"]/following-sibling::label')))
    make_executable_checkbox.click()

    input_text = 'Test123'
    wrapper_location = browser.find_element(By.CSS_SELECTOR, 'input[name="_.wrapperLocation"]')
    wrapper_location.send_keys(input_text)

    tasks = browser.find_element(By.CSS_SELECTOR, 'input[name="_.tasks"]')
    tasks.send_keys(input_text)

    advanced_invoke_gradle = wait10.until(element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div/div[4]/div[4]/div[1]/button')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_invoke_gradle)
    advanced_invoke_gradle.click()

    switches = wait10.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="_.switches"]')))
    switches.send_keys(input_text)

    sys_properties = browser.find_element(By.CSS_SELECTOR, 'textarea[name="_.systemProperties"]')
    sys_properties.send_keys(input_text)

    pass_all_checkbox = wait10.until(element_to_be_clickable((By.XPATH, '//input[@name="_.passAllAsSystemProperties"]/following-sibling::label')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pass_all_checkbox)
    pass_all_checkbox.click()

    project_prop = browser.find_element(By.CSS_SELECTOR, 'textarea[name="_.projectProperties"]')
    project_prop.send_keys(input_text)

    pass_all_checkbox2 = wait10.until(element_to_be_clickable((By.XPATH, '//input[@name="_.passAllAsProjectProperties"]/following-sibling::label')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", pass_all_checkbox2)
    pass_all_checkbox2.click()

    root_build_script = browser.find_element(By.CSS_SELECTOR, 'input[name="_.rootBuildScriptDir"]')
    root_build_script.send_keys(input_text)

    build_file = browser.find_element(By.CSS_SELECTOR, 'input[name="_.buildFile"]')
    build_file.send_keys(input_text)

    use_workspace_checkbox = wait10.until(element_to_be_clickable((By.XPATH, '//input[@name="_.useWorkspaceAsHome"]/following-sibling::label')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", use_workspace_checkbox)
    use_workspace_checkbox.click()

    add_build_steps.click()
    set_building_status_dropdown = browser.find_element(By.XPATH, '//*[@id="tippy-5"]/div/div/div/div[2]/button[7]')
    set_building_status_dropdown.click()

    commit_context = browser.find_element(By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div[2]/div[3]/div[1]/div[2]/select')
    commit_context.click()

    manually_entered = browser.find_element(By.XPATH, '//option[text()="Manually entered context name"]')
    manually_entered.click()

    context_name = browser.find_element(By.CSS_SELECTOR, 'input[name="_.context"]')
    context_name.send_keys(input_text)

    advanced_set_building_status = wait10.until(element_to_be_clickable((By.XPATH, '//*[@id="main-panel"]/form/div[1]/section[5]/div[3]/div[2]/div[3]/div[3]/div[1]/button')))
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_set_building_status)
    advanced_set_building_status.click()

    content = browser.find_element(By.CSS_SELECTOR, 'input[name="_.content"]')
    content.send_keys(input_text)

    save_button = browser.find_element(By.NAME, 'Submit')
    save_button.click()

    wait10.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), item_name))
    assert item_name in browser.find_element(By.TAG_NAME, "h1").text
