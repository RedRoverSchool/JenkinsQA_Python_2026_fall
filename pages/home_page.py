from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from pages.multiconfiguration_project_page import MulticonfigurationProjectPage
from pages.new_item_page import NewItemPage
from pages.manage_jenkins_page import ManageJenkinsPage
from pages.freestyle_project_page import FreestyleProjectPage
from pages.pipeline_page import PipelinePage
from pages.rename_page import RenamePage
from pages.base_item_page import BaseItemPage
from pages.pipeline_configuration_page import PipelineConfigurationPage

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
    BUILD_QUEUE = (By.ID, "buildQueue")
    BUILD_QUEUE_TOGGLE = (By.XPATH, "//a[contains(@href,'buildQueue')]")
    BUILD_QUEUE_CONTENT = (By.XPATH, "//td[text()='No builds in the queue.']")
    MAIN_PANEL = (By.ID, "main-panel")
    PROJECT_LINKS = (By.XPATH, "//table[@id='projectstatus']//a[contains(@class,'jenkins-table__link')]")
    JOB_NAME = (By.XPATH, "//*[@id='job_random_name']/td[3]/a/span")
    DROPDOWN_CHEVRON = (By.XPATH, f"//*[@id='job_random_name']/td[3]/a/button")
    DROPDOWN_CONFIGURE = (By.XPATH, "//*[@id='tippy-4']/div/div/div/a[2]")

    def get_welcome_title(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.WELCOME_TITLE)
        ).text

    def get_first_project_name(self) -> str:
        return self.wait5.until(
            EC.visibility_of_element_located(self.FIRST_PROJECT_NAME)
        ).text

    def is_project_present(self, project_name) -> bool:
        if "Welcome to Jenkins!" in self.driver.find_element(*self.MAIN_PANEL).text:
            return False
        project_names = [el.text for el in self.driver.find_elements(*self.PROJECT_LINKS)]
        return project_name in project_names

    def get_multiconfiguration_project(self, project_name: str) -> MulticonfigurationProjectPage:
        self.driver.find_element(By.LINK_TEXT, project_name).click()

        return MulticonfigurationProjectPage(self.driver)

    def click_new_item(self) -> NewItemPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.NEW_ITEM_LINK)
        ).click()

        return NewItemPage(self.driver)

    def click_create_job(self) -> NewItemPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.CREATE_JOB_LINK)
        ).click()

        return NewItemPage(self.driver)

    def click_manage_jenkins(self) -> ManageJenkinsPage:
        self.wait5.until(
            EC.element_to_be_clickable(self.MANAGE_JENKINS_LINK)
        ).click()

        return ManageJenkinsPage(self.driver)

    def toggle_build_queue(self):
        switcher = self.wait5.until(EC.element_to_be_clickable(self.BUILD_QUEUE_TOGGLE))
        switcher.click()
        self.wait5.until(EC.staleness_of(switcher))
        return self

    def is_build_queue_expanded(self) -> bool:
        expand_collapse = self.wait5.until(
            EC.element_to_be_clickable(self.BUILD_QUEUE_TOGGLE)
        )
        if expand_collapse.get_attribute("title") == "collapse":
            return True
        return False

    def is_build_queue_content_displayed(self) -> bool:
        return "No builds in the queue." in self.driver.find_element(*self.BUILD_QUEUE).text

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

    def is_add_description_displayed(self) -> bool:
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

    def click_job(self, job_name) -> BaseItemPage:
        job_locator = (By.LINK_TEXT, job_name)
        self.wait5.until(
            EC.element_to_be_clickable(job_locator)
        ).click()

        return BaseItemPage(self.driver)

    def click_project_context_menu_and_click_rename(self,project_name):
        chevron_selector = f"//button[@class='jenkins-menu-dropdown-chevron' and contains(@data-href,{project_name})]"
        self.driver.find_element(By.XPATH, chevron_selector).click()
        self.wait10.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'confirm-rename')]"))
        ).click()

        return RenamePage(self.driver)

    def click_pipeline(self, pipeline_name: str) -> PipelinePage:
        pipeline_locator = (By.CSS_SELECTOR, f"[href='job/{pipeline_name}/']")

        self.wait10.until(
            EC.element_to_be_clickable(pipeline_locator)
        ).click()

        return PipelinePage(self.driver)

    def is_project_displayed(self, project_name: str) -> bool:
        project_locator = (By.LINK_TEXT, project_name)

        return self.wait10.until(
            EC.visibility_of_element_located(project_locator)
        ).is_displayed()

    def is_project_absent(self, project_name: str) -> bool:

        try:
            self.wait5.until(EC.invisibility_of_element_located((By.XPATH, f"//table[@id='projectstatus']//a[normalize-space(.)={project_name}]")))
            return True
        except TimeoutException:
            return False

    def open_configuration_via_dropdown(self, job_name: str) -> PipelineConfigurationPage:
        job_element = self.wait10.until(EC.visibility_of_element_located(JOB_NAME))
        actions = ActionChains(self.driver)
        actions.move_to_element(job_element).perform()
        self.wait10.until(EC.element_to_be_clickable(DROPDOWN_CHEVRON)).click()
        self.wait10.until(EC.element_to_be_clickable(DROPDOWN_CONFIGURE)).click()
        self.wait10.until(EC.url_contains("configure"))
        return PipelineConfigurationPage(self.driver)
