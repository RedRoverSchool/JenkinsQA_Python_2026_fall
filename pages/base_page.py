from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.base_model import BaseModel

if TYPE_CHECKING:
    from pages.home_page import HomePage


class BasePage(BaseModel):
    JENKINS_LOGO = (By.CLASS_NAME, "app-jenkins-logo")
    BREADCRUMBS = (By.CLASS_NAME, "jenkins-breadcrumbs__list")
    DELETE_MODAL = (By.CSS_SELECTOR, "dialog[open], .jenkins-modal")
    CONFIRM_DELETE_BTN = (By.XPATH, ".//button[@data-id='ok']")
    CANCEL_DELETE_BTN = (By.CSS_SELECTOR, "button[data-id='cancel']")

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