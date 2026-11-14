from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def test_user_dropdown_menu (browser):
    dropdown = browser.find_element(
        By.XPATH, '//*[@id="root-action-UserAction"]'
    )

    actions = ActionChains(browser)
    actions.move_to_element(dropdown).perform()

    assert dropdown.is_enabled()
    assert dropdown.get_attribute("aria-expanded") == "true"
