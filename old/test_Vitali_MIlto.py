from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_first():
    driver = webdriver.Chrome()

    driver.get("https://automationteststore.com/index.php?rt=product/search&keyword=men&category_id=0")

    title = driver.title

    driver.implicitly_wait(5)

    text_box = driver.find_element(by=By.NAME, value="filter_keyword")
    # pass_box = driver.find_element(by=By.NAME, value="my-password")
    search_button = driver.find_element(By.CSS_SELECTOR, "div.button-in-search")

    text_box.send_keys("Womens high heel point toe stiletto sandals ankle strap court shoes")
    # pass_box.send_keys("12345")
    search_button.click()

    current_url = driver.current_url
    assert "product_id=118" in current_url

    driver.quit()


def test_second ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    driver.implicitly_wait(5)
    trails = driver.find_element(By.LINK_TEXT, "Trails")
    trails.click()
    course = driver.find_element(By.XPATH, '//*[@id="course-grid"]/div[1]/div[2]/a/div[1]/h3')
    course.click()
    page_title = driver.find_element(By. CSS_SELECTOR, "h1.course-detail-title")
    assert page_title.text == "Git Teamwork for QA: Branching, Merging & Pull Requests"
    driver.quit()

def wrong_login ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    driver.implicitly_wait(10)
    login = driver.find_element(By.LINK_TEXT, "Login")
    login.click()

def login_open ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    driver.implicitly_wait(3)
    login = driver.find_element(By.LINK_TEXT, "Login")
    login.click()
    driver.quit()

def tes_only_email ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    driver.implicitly_wait(3)
    email_filed = driver.find_element(By.ID, 'login-email')
    email_filed.send_keys("123@gmailllll.com")
    login_button = driver.find_element(By.CSS_SELECTOR, 'auth-submit-label')
    login_button.click()

def test_wron_data():
        driver = webdriver.Chrome()
        driver.get("https://bugeater.web.app/")
        driver.implicitly_wait(15)
        login_link = driver.find_element(By.LINK_TEXT, "Login")
        login_link.click()

        email_field = driver.find_element(By.ID, "login-email")
        email_field.send_keys("123@gmail.com")
        pass_field = driver.find_element(By.ID, "login-password")
        pass_field.send_keys("1234")

        login_button = driver.find_element(By.CSS_SELECTOR, "button.auth-submit")
        login_button.click()

        error = driver.find_element(By.ID, "login-feedback-chip")


        driver.quit()
def test_theme_change ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    theme = driver.find_element(By.CSS_SELECTOR,'button[aria-label="Toggle theme"]' )
    theme.click()
    time.sleep(1)
    theme.click()
    driver.quit()

def test_explore_trials ():
    driver = webdriver.Chrome()
    driver.get("https://bugeater.web.app/")
    driver.implicitly_wait(10)
    explore_trials = driver.find_element(By.CSS_SELECTOR, "a[href='#featured-trails']")
    explore_trials.click()
