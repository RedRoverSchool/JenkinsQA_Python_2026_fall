from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.new_item_page import NewItemPage
from pages.manage_jenkins_page import ManageJenkinsPage
from pages.freestyle_project_page import FreestyleProjectPage


class HomePage(BasePage):
    WELCOME_TITLE = (By.XPATH, "//div[@class='empty-state-block']/h1")
    NEW_ITEM_LINK = (By.XPATH, "//a[@href='/view/all/newJob']")
    MANAGE_JENKINS_LINK = (By.XPATH, "//a[contains(@id,'ManageJenkinsAction')]")
    FIRST_PROJECT_NAME = (By.CSS_SELECTOR, ".jenkins-table__link >span:first-child")
    CREATE_JOB_LINK = (By.XPATH, "//a[@href='newJob']")
    SETUP_AGENT_LINK = (By.XPATH, "//a[@href='computer/new']")
    CONFIGURE_CLOUD_LINK = (By.XPATH, "//a[@href='cloud/']")
    LEARN_MORE_LINK = (By.XPATH, "//a[contains(@href,'jenkins.io')]")
    ADD_DESCRIPTION_LINK = (By.ID, "description-link")

    def get_welcome_title(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.WELCOME_TITLE)
        ).text

    def get_first_project_name(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.FIRST_PROJECT_NAME)
        ).text

    def click_new_item(self) -> NewItemPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.NEW_ITEM_LINK)
        ).click()

        return NewItemPage(self.driver)

    def click_manage_jenkins(self) -> ManageJenkinsPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.MANAGE_JENKINS_LINK)
        ).click()

        return ManageJenkinsPage(self.driver)

    def is_create_job_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.CREATE_JOB_LINK)
        ).is_displayed()

    def is_setup_agent_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.SETUP_AGENT_LINK)
        ).is_displayed()

    def is_configure_cloud_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.CONFIGURE_CLOUD_LINK)
        ).is_displayed()

    def is_learn_more_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.LEARN_MORE_LINK)
        ).is_displayed()

    def is_add_description_displayed(self):
        return self.wait5.until(
            EC.visibility_of_element_located(self.ADD_DESCRIPTION_LINK)
        ).is_displayed()

    def is_new_item_displayed(self) -> bool:
        return self.wait5.until(
            EC.visibility_of_element_located(self.NEW_ITEM_LINK)
        ).is_displayed()

    def click_project(self, project_name: str) -> FreestyleProjectPage:
        project_locator = (By.LINK_TEXT, project_name)

        self.wait10.until(
            EC.element_to_be_clickable(project_locator)
        ).click()

        return FreestyleProjectPage(self.driver)