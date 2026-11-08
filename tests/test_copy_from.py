from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

class PageLocators:
    JENKINS_LOGO = (By.CLASS_NAME, "app-jenkins-logo")

    MAIN_NEW_ITEM = (By.CSS_SELECTOR, "a[href='/view/all/newJob']")

    NEW_ITEM_NAME_INPUT = (By.ID, "name")
    NEW_ITEM_TYPE_PIPELINE = (By.CLASS_NAME, "org_jenkinsci_plugins_workflow_job_WorkflowJob")
    NEW_ITEM_OK_BUTTON = (By.ID, "ok-button")
    NEW_ITEM_TYPE_DUPLICATE = (By.ID, "duplicate-job")
    NEW_ITEM_DUPLICATE_INPUT = (By.ID, "from")
    NEW_ITEM_DROPDOWN_VALUES = (By.CSS_SELECTOR, "button.jenkins-dropdown__item")

    CONFIGURE_GENERAL_DESCRIPTION_INPUT = (By.NAME, "description")
    CONFIGURE_GENERAL_SAVE_BUTTON = (By.NAME, "Submit")

class Inputs:
    FIRST_JOB_NAME_VALID = "First Job"
    SECOND_JOB_NAME_VALID = "Second Job"

    MAIN_CREATED_JOB_TEMPLATE = "job_{}"

    DESCRIPTION_TEXT_VALID = "Description"


class PageActions:
    def __init__(self, wait):
        self.wait = wait

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator),
                           message=f"Not clickable: {locator}").click()

    def visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator),
                           message=f"Not visible: {locator}")

    def enter_text(self, input, text):
        return input.send_keys(text)

    def wait_url_not_contains(self, text):
        self.wait.until_not(EC.url_contains(text),
                           message=f"URL not contains: {text}")


@pytest.fixture
def actions(wait5):
    return PageActions(wait5)


@pytest.fixture
def create_item_with_configuration(browser, actions):
    actions.click(PageLocators.MAIN_NEW_ITEM)
    actions.enter_text(actions.visibility(PageLocators.NEW_ITEM_NAME_INPUT), Inputs.FIRST_JOB_NAME_VALID)
    actions.click(PageLocators.NEW_ITEM_TYPE_PIPELINE)
    actions.click(PageLocators.NEW_ITEM_OK_BUTTON)
    actions.enter_text(actions.visibility(PageLocators.CONFIGURE_GENERAL_DESCRIPTION_INPUT), Inputs.DESCRIPTION_TEXT_VALID)
    actions.click(PageLocators.CONFIGURE_GENERAL_SAVE_BUTTON)
    actions.wait_url_not_contains("configure")
    actions.click(PageLocators.JENKINS_LOGO)




def test_dropdown_shows_matching_existing_items(browser, actions, create_item_with_configuration):
    actions.click(PageLocators.MAIN_NEW_ITEM)
    actions.click(PageLocators.NEW_ITEM_TYPE_PIPELINE)
    actions.enter_text(actions.visibility(PageLocators.NEW_ITEM_NAME_INPUT), Inputs.SECOND_JOB_NAME_VALID)

    actions.click(PageLocators.NEW_ITEM_TYPE_DUPLICATE)
    actions.enter_text(actions.visibility(PageLocators.NEW_ITEM_DUPLICATE_INPUT), Inputs.FIRST_JOB_NAME_VALID)
    #actions.visibility(PageLocators.NEW_ITEM_COPY_FROM_DROPDOWN_ITEM)
    options = browser.find_elements(*PageLocators.NEW_ITEM_DROPDOWN_VALUES)

    assert Inputs.FIRST_JOB_NAME_VALID in [o.text for o in options]

