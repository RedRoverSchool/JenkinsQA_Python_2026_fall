from selenium import webdriver
from selenium.webdriver.common.by import By
#def test_first():
#    driver = webdriver.Chrome()
#
#    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
#
#    title = driver.title
#
#    driver.implicitly_wait(0.5)
#
#    text_box = driver.find_element(by=By.NAME, value="my-text")
#    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
#
#    text_box.send_keys("Selenium")
#    submit_button.click()
#
#    message1 = driver.find_element(by=By.ID, value="message")
#    assert message1.text == "Received! "
#
#    driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
def test_second():
    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    title = driver.title

    driver.implicitly_wait(0.5)

    text_box1 = driver.find_element(by=By.NAME, value="user-name")
    text_box2 = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="login-button")

    text_box1.send_keys("standard_user")
    text_box2.send_keys("secret_sauce")
    submit_button.click()

    message2 = driver.find_element(by=By.CLASS_NAME, value="app_logo")
    assert message2.text == "Swag Labs"

    driver.quit()

def test_three():
    driver = webdriver.Chrome()

    driver.get("https://www.saucedemo.com/")

    title = driver.title

    driver.implicitly_wait(0.5)

    text_box1 = driver.find_element(by=By.NAME, value="user-name")
    text_box2 = driver.find_element(by=By.NAME, value="password")
    submit_button = driver.find_element(by=By.NAME, value="login-button")


    text_box1.send_keys("standard_user")
    text_box2.send_keys("secret_sauce")
    submit_button.click()
    cart_button = driver.find_element(by=By.NAME, value="add-to-cart-sauce-labs-backpack")
    cart_button.click()

    message3 = driver.find_element(by=By.NAME, value="remove-sauce-labs-backpack")
    assert message3.text == "Remove"
    assert "/inventory.html" in driver.current_url
    driver.quit()


def test_four():
   driver = webdriver.Chrome()

   driver.get("https://www.saucedemo.com/")

   title = driver.title

   driver.implicitly_wait(0.5)

   text_box1 = driver.find_element(by=By.NAME, value="user-name")
   text_box2 = driver.find_element(by=By.NAME, value="password")
   submit_button = driver.find_element(by=By.NAME, value="login-button")


   text_box1.send_keys("standard_user")
   text_box2.send_keys("secret_sauce")
   submit_button.click()

   add_to_cart_button = driver.find_element(by=By.NAME, value="add-to-cart-sauce-labs-backpack")
   add_to_cart_button.click()

   cart_button = driver.find_element(by=By.CLASS_NAME, value="shopping_cart_container")
   cart_button.click()

   cart_quantity = driver.find_element(by=By.CSS_SELECTOR, value=".cart_quantity")

   assert cart_quantity.text == "1"
   driver.quit()