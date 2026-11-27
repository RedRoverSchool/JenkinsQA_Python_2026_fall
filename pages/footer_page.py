from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.rest_api_page import RestApiPage
from pages.about_page import AboutPage
from pages.jenkins_site_page import JenkinsSitePage


class Footer(BasePage):
    FOOTER = (By.TAG_NAME, "footer")
    REST_API_LINK = (By.XPATH, "//footer//a[@href='api/']")
    JENKINS_VERSION_LINK = (By.XPATH, "//button[contains(@class,'jenkins_ver')]")
    VERSION_DROPDOWN_ITEMS = (By.XPATH, "//div[starts-with(@id,'tippy')]//a[contains(@class,'jenkins-dropdown__item')]")
    ABOUT_JENKINS = (By.XPATH, "//div[starts-with(@id,'tippy')]//a[contains(@href,'/about')]")
    GET_INVOLVED = (By.XPATH, "//div[starts-with(@id,'tippy')]//a[contains(., 'Get involved')]")
    WEBSITE_LINK = (By.XPATH, "//div[starts-with(@id,'tippy')]//a[contains(., 'Website')]")

    def is_footer_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.FOOTER)
        ).is_displayed()

    def get_jenkins_version(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.JENKINS_VERSION_LINK)
        ).text.strip()

    def click_rest_api(self) -> RestApiPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.REST_API_LINK)
        ).click()

        return RestApiPage(self.driver)

    def click_jenkins_version(self):
        self.wait5.until(
            EC.element_to_be_clickable(self.JENKINS_VERSION_LINK)
        ).click()
        self.wait5.until(
            EC.visibility_of_all_elements_located(self.VERSION_DROPDOWN_ITEMS)
        )
        return self

    def get_version_dropdown_items(self) -> list[str]:
        items = self.wait5.until(
            EC.visibility_of_all_elements_located(self.VERSION_DROPDOWN_ITEMS)
        )
        return [item.text.strip() for item in items]

    def click_about_jenkins(self) -> AboutPage:
        self.click_jenkins_version()
        self.wait5.until(
            EC.element_to_be_clickable(self.ABOUT_JENKINS)
        ).click()

        return AboutPage(self.driver)

    def click_get_involved(self) -> JenkinsSitePage:
        self.click_jenkins_version()
        self.wait5.until(
            EC.element_to_be_clickable(self.GET_INVOLVED)
        ).click()

        return JenkinsSitePage(self.driver)

    def click_website(self) -> JenkinsSitePage:
        self.click_jenkins_version()
        self.wait5.until(
            EC.element_to_be_clickable(self.WEBSITE_LINK)
        ).click()

        return JenkinsSitePage(self.driver)
