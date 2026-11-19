from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from common.base_model import BaseModel

if TYPE_CHECKING:
    from pages.home_page import HomePage


class BasePage(BaseModel):
    def goto_home_page(self) -> HomePage:
        from pages.home_page import HomePage

        self.driver.find_element(By.CLASS_NAME, "app-jenkins-logo").click()

        return HomePage(self.driver)
