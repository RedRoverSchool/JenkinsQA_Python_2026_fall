from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from common.project_utils import get_url


def open_user_dropdown_menu(browser, wait2):

    user_menu_btn = browser.find_element(By.ID, "root-action-UserAction")
    ActionChains(browser).move_to_element(user_menu_btn).perform()
    wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-tippy-root] .jenkins-dropdown")))


def test_redirect_to_login_page_after_logout(browser, wait2):

    open_user_dropdown_menu(browser, wait2)
    browser.find_element(By.XPATH, '//a[@href="/logout"]').click()

    assert len(browser.find_elements(By.CSS_SELECTOR, ".jenkins-dialog, .modal, .warning, .error")) == 0
    assert wait2.until(EC.presence_of_element_located((By.ID, "j_username"))).get_attribute("value") == ""
    assert browser.find_element(By.ID, "j_password").get_attribute("value") == ""


def test_check_no_access_to_protected_page_after_logout(browser, wait2):

    open_user_dropdown_menu(browser, wait2)
    browser.find_element(By.XPATH, '//a[@href="/logout"]').click()

    browser.get(get_url() + "/view/all/builds")
    wait2.until(EC.invisibility_of_element_located((By.ID, "projectStatus")))


def test_cancel_sign_out_by_closing_menu(browser, wait2):

    open_user_dropdown_menu(browser, wait2)
    body = browser.find_element(By.TAG_NAME, "body")
    ActionChains(browser).move_to_element_with_offset(body, 10, 10).perform()

    assert wait2.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.jenkins-dropdown")))
    assert browser.find_element(By.ID, "root-action-UserAction").is_displayed()


def test_check_access_to_protected_page_after_canceling_logout(browser, wait2):

    open_user_dropdown_menu(browser, wait2)
    body = browser.find_element(By.TAG_NAME, "body")
    ActionChains(browser).move_to_element_with_offset(body, 10, 10).perform()

    browser.get(get_url() + "/view/all/builds")
    wait2.until(EC.presence_of_element_located((By.ID, "projectStatus")))
