from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.pipeline_page import PipelinePage


class PipelineConfigurationPage(BasePage):
    def click_save(self) -> PipelinePage:
        from pages.pipeline_page import PipelinePage

        self.driver.find_element(By.NAME, "Submit").click()

        return PipelinePage(self.driver)
