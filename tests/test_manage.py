from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_open_page(browser, wait10):
    manage_button = wait10.until(EC.element_to_be_clickable((By.ID, "root-action-ManageJenkinsAction")))
    manage_button.click()

    manage_heading = wait10.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))

    plugin_item = browser.find_element(By.CSS_SELECTOR, 'a[href="pluginManager"]')

    assert manage_heading.text == "Manage Jenkins"
    assert plugin_item.is_displayed()