from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_configuration_page import BaseConfigurationPage

class MultibranchConfigurationPage(BaseConfigurationPage):
    HEALTH_METRICS_BTN = (By.XPATH, "//button[contains(@class, 'advancedButton')]")
    ADD_METRIC_BTN = (By.XPATH, "//button[@suffix='healthMetrics']")
    METRICS_DROPDOWN_MENU = (By.CSS_SELECTOR, "div[id^='tippy'] .jenkins-dropdown")
    METRICS_DROPDOWN_ITEMS = (By.CSS_SELECTOR, "div[id^='tippy'] .jenkins-dropdown__item")
    CHILD_NAME_INPUT = (By.XPATH, "//input[@name='_.childName']")
    RECURSIVE_CHECKBOX = (By.XPATH, "//input[@name='_.recursive']")
    PRIMARY_BRANCH_METRIC = (By.XPATH, "//div[contains(@descriptorid,'PrimaryBranchHealthMetric')]")

    def open_health_metrics_dropdown(self):
        health_metrics_btn = self.wait5.until(
            EC.element_to_be_clickable(self.HEALTH_METRICS_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
        health_metrics_btn.click()

        self.wait5.until(
            EC.element_to_be_clickable(self.ADD_METRIC_BTN)
        ).click()

        self.wait5.until(
            EC.visibility_of_element_located(self.METRICS_DROPDOWN_MENU)
        )
        return self

    def expand_health_metrics(self):
        health_metrics_btn = self.wait5.until(
            EC.element_to_be_clickable(self.HEALTH_METRICS_BTN)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", health_metrics_btn)
        health_metrics_btn.click()
        return self

    def open_metrics_dropdown(self):
        add_metric_btn = self.wait5.until(EC.element_to_be_clickable(self.ADD_METRIC_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_metric_btn)
        add_metric_btn.click()
        self.wait5.until(
            EC.visibility_of_all_elements_located(self.METRICS_DROPDOWN_ITEMS)
        )
        return self

    def get_available_health_metrics(self) -> list[str]:
        items = self.wait5.until(
            EC.visibility_of_all_elements_located(self.METRICS_DROPDOWN_ITEMS)
        )
        return [item.text.strip() for item in items if item.is_enabled()]


    def select_health_metric(self, metric_name: str):
        metric_locator = (By.XPATH, f"//div[starts-with(@id, 'tippy')]//button[contains(@class, 'jenkins-dropdown__item') "
                                    f"and contains(., '{metric_name}')]")
        self.wait5.until(
            EC.element_to_be_clickable(metric_locator)
        ).click()
        return self

    def is_child_name_input_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.CHILD_NAME_INPUT)
        ).is_displayed()

    def is_recursive_checkbox_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.RECURSIVE_CHECKBOX)
        ).is_displayed()

    def is_recursive_checkbox_selected(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.RECURSIVE_CHECKBOX)
        ).is_selected()

    def is_primary_branch_metric_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.PRIMARY_BRANCH_METRIC)
        ).is_displayed()

    def is_add_metric_btn_enabled(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.ADD_METRIC_BTN)
        ).is_enabled()
