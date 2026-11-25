from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from common.base_model import BaseModel

if TYPE_CHECKING:
    from pages.home_page import HomePage


class BasePage(BaseModel):
    JENKINS_LOGO = (By.CLASS_NAME, "app-jenkins-logo")
    BREADCRUMBS = (By.CLASS_NAME, "jenkins-breadcrumbs__list")
    DELETE_MODAL = (By.CSS_SELECTOR, "dialog[open], .jenkins-modal")
    CONFIRM_DELETE_BTN = (By.XPATH, ".//button[@data-id='ok']")
    CANCEL_DELETE_BTN = (By.CSS_SELECTOR, "button[data-id='cancel']")
    BODY = (By.TAG_NAME, "body")

    def goto_home_page(self) -> HomePage:
        from pages.home_page import HomePage
        self.driver.find_element(*self.JENKINS_LOGO).click()
        return HomePage(self.driver)

    def refresh_page(self):
        self.driver.refresh()
        return self

    def get_breadcrumbs_text(self) -> str:
        return self.wait10.until(
            EC.visibility_of_element_located(self.BREADCRUMBS)
        ).text

    def confirm_delete_modal(self):
        modal = self.wait5.until(
            EC.visibility_of_element_located(self.DELETE_MODAL)
        )

        self.wait5.until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_BTN)
        ).click()

        self.wait5.until(
            EC.invisibility_of_element_located(modal)
        )
        from pages.home_page import HomePage
        return HomePage(self.driver)

    def cancel_delete_modal(self):
        modal = self.wait5.until(
            EC.visibility_of_element_located(self.DELETE_MODAL)
        )

        self.wait5.until(
            EC.element_to_be_clickable(self.CANCEL_DELETE_BTN)
        ).click()

        self.wait5.until(
            EC.invisibility_of_element_located(modal)
        )
        return self

    def wait_for_element_visible(self, locator):
        return self.wait10.until(EC.visibility_of_element_located(locator))

    def click_clear_and_send_keys_in_field_area(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.click()
        element.clear()
        element.send_keys(text)
        return self
    def click_btn(self, locator):
        btn = self.wait10.until(EC.element_to_be_clickable(locator))
        btn.click()
        return self

    def wait_for_text_in_element(self, locator: tuple, text: str):
        self.wait10.until(EC.text_to_be_present_in_element(locator, text))
        return self

    def get_element_text(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        return element.text.strip()

    def clear_field(self, locator):
        textarea = self.wait10.until(EC.element_to_be_clickable(locator))
        textarea.click()
        textarea.send_keys(Keys.CONTROL, "a")
        textarea.send_keys(Keys.BACKSPACE)
        self.wait10.until(lambda driver: textarea.get_attribute("value") == "")
        return self

    def enter_text(self, locator: tuple, text: str) -> "BasePage":
        element = self.wait10.until(EC.visibility_of_element_located(locator))
        element.click()
        element.clear()
        element.send_keys(text)
        return self
