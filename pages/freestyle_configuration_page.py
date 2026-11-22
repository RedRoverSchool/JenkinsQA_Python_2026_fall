from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.freestyle_project_page import FreestyleProjectPage


class FreestyleConfigurationPage(BasePage):
    ENVIRONMENT_BUTTON = (
        By.XPATH,
        "//button[.//span[normalize-space()='Environment']]"
    )
    ENVIRONMENT_OPTIONS = [
        (By.ID, "cb18"),
        (By.ID, "cb19"),
        (By.ID, "cb21"),
        (By.ID, "cb22"),
        (By.ID, "cb23"),
        (By.NAME, "hudson-tasks-AntWrapper"),
    ]

    SCM_BUTTON = (
        By.XPATH,
        "//button[.//span[normalize-space()='Source Code Management']]"
    )
    SCM_OPTIONS = [
        (By.CSS_SELECTOR, "label[for='radio-block-0']"),
        (By.CSS_SELECTOR, "label[for='radio-block-1']"),
    ]
    GIT_OPTION = (By.CSS_SELECTOR, "label[for='radio-block-1']")
    GIT_FIELDS = [
        (By.CSS_SELECTOR, "input[name='_.url']"),
        (By.CSS_SELECTOR, "select[name='_.credentialsId']"),
        (By.CSS_SELECTOR, "input[name='_.name'][default='*/master']"),
    ]
    REPOSITORY_URL = (By.CSS_SELECTOR, "input[name='_.url']")
    GIT_ERROR_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'error') and contains(., 'Failed to connect to repository')]"
    )

    BUILD_TRIGGERS_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'jenkins-section__title') and normalize-space()='Triggers']"
    )
    BUILD_TRIGGER_OPTIONS = [
        (By.ID, "cb13"),
        (By.ID, "cb14"),
        (By.ID, "cb15"),
        (By.ID, "cb16"),
        (By.ID, "cb17"),
    ]
    REMOTE_BUILD_TRIGGER = (By.ID, "cb13")
    REMOTE_BUILD_TRIGGER_LABEL = (
        By.XPATH,
        "//span[contains(@class, 'jenkins-checkbox')][.//input[@id='cb13']]//label"
    )
    AUTH_TOKEN_FIELD = (By.NAME, "authToken")

    BUILD_PERIODICALLY = (By.ID, "cb15")
    BUILD_PERIODICALLY_SCHEDULE = (
        By.CSS_SELECTOR,
        "textarea[name='_.spec']"
    )
    POLL_SCM = (By.ID, "cb17")
    POLL_SCM_LABEL = (
        By.XPATH,
        "//label[contains(., 'Poll SCM')]"
    )
    POLL_SCM_SCHEDULE = (
        By.XPATH,
        "//label[contains(., 'Poll SCM')]/following::textarea[1]"
    )
    BUILD_AFTER_PROJECTS = (By.ID, "cb14")
    BUILD_AFTER_PROJECTS_LABEL = (
        By.XPATH,
        "//label[contains(., 'Build after other projects are built')]"
    )
    PROJECTS_TO_WATCH = (By.NAME, "_.upstreamProjects")
    SUCCESS_THRESHOLD = (
        By.CSS_SELECTOR,
        "input[name='ReverseBuildTrigger.threshold'][value='SUCCESS']"
    )
    UNSTABLE_THRESHOLD = (
        By.XPATH,
        "//div[contains(@class, 'jenkins-radio')][.//input[@value='UNSTABLE']]/label"
    )
    FAILURE_THRESHOLD = (
        By.XPATH,
        "//div[contains(@class, 'jenkins-radio')][.//input[@value='FAILURE']]/label"
    )
    ABORTED_THRESHOLD = (
        By.XPATH,
        "//div[contains(@class, 'jenkins-radio')][.//input[@value='ABORTED']]/label"
    )
    BUILD_PERIODICALLY_HELP = (
        By.CSS_SELECTOR,
        "a[aria-label='Help for feature: Build periodically']"
    )
    POLL_SCM_HELP = (
        By.CSS_SELECTOR,
        "a[aria-label='Help for feature: Poll SCM']"
    )
    BUILD_AFTER_PROJECTS_HELP = (
        By.CSS_SELECTOR,
        "a[aria-label='Help for feature: Build after other projects are built']"
    )
    POST_BUILD_ACTIONS_BUTTON = (
        By.XPATH,
        "//button[.//span[normalize-space()='Post-build Actions']]"
    )
    ADD_POST_BUILD_ACTION_BUTTON = (
        By.CSS_SELECTOR,
        "button.hetero-list-add[suffix='publisher']"
    )
    POST_BUILD_ACTION_ITEMS = (
        By.CSS_SELECTOR,
        "button.jenkins-dropdown__item"
    )
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[name='Submit'][value='Save']")
    APPLY_BUTTON = (By.CSS_SELECTOR, "button[name='Apply']")

    def click_environment(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.ENVIRONMENT_BUTTON)
        ).click()

        return self

    def are_environment_options_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.ENVIRONMENT_OPTIONS
        )

    def are_environment_options_unselected(self) -> bool:
        return all(
            not self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_selected()
            for locator in self.ENVIRONMENT_OPTIONS
        )

    def click_scm(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.SCM_BUTTON)
        ).click()

        return self

    def are_scm_options_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.SCM_OPTIONS
        )

    def is_none_scm_selected(self) -> bool:
        return self.wait10.until(
            EC.presence_of_element_located((By.ID, "radio-block-0"))
        ).is_selected()

    def select_git_scm(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.GIT_OPTION)
        ).click()

        return self

    def are_git_fields_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in self.GIT_FIELDS
        )

    def enter_repository_url(self, repository_url: str) -> FreestyleConfigurationPage:
        url_field = self.wait10.until(
            EC.visibility_of_element_located(self.REPOSITORY_URL)
        )
        url_field.send_keys(repository_url)
        url_field.send_keys("\t")

        return self

    def is_git_error_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.GIT_ERROR_MESSAGE)
        ).is_displayed()

    def click_save(self) -> FreestyleProjectPage:
        from pages.freestyle_project_page import FreestyleProjectPage

        self.driver.find_element(By.NAME, "Submit").click()
        self.wait10.until(
            EC.presence_of_element_located((By.ID, "description-link"))
        )

        return FreestyleProjectPage(self.driver)

    def is_enable_disable_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located((By.ID, "enable-disable-project"))
        ).is_selected()

    def is_enable_disable_displayed(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located((By.ID, "enable-disable-project"))
        ).is_displayed()

    def disable_project(self) -> FreestyleConfigurationPage:
        self.driver.find_element(
            By.CSS_SELECTOR, "label[for='enable-disable-project']"
        ).click()

        return self

    def click_build_triggers(self) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.element_to_be_clickable(self.BUILD_TRIGGERS_BUTTON)
        ).click()

        return self

    def enable_remote_build_trigger(self) -> FreestyleConfigurationPage:
        remote_trigger_label = self.wait10.until(
            EC.presence_of_element_located(self.REMOTE_BUILD_TRIGGER_LABEL)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            remote_trigger_label
        )

        remote_trigger = self.wait10.until(
            EC.presence_of_element_located(self.REMOTE_BUILD_TRIGGER)
        )

        self.wait10.until(
            EC.element_to_be_selected(remote_trigger)
        )

        return self

    def enter_authentication_token(self, token: str) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.visibility_of_element_located(self.AUTH_TOKEN_FIELD)
        ).send_keys(token)

        return self

    def are_build_trigger_options_available(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_enabled()
            for locator in self.BUILD_TRIGGER_OPTIONS
        )

    def are_build_trigger_options_unselected(self) -> bool:
        return all(
            not self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_selected()
            for locator in self.BUILD_TRIGGER_OPTIONS
        )

    def is_remote_build_trigger_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.REMOTE_BUILD_TRIGGER)
        ).is_selected()

    def enable_build_periodically(self) -> FreestyleConfigurationPage:
        build_periodically = self.wait10.until(
            EC.presence_of_element_located(self.BUILD_PERIODICALLY)
        )

        if not build_periodically.is_selected():
            self.driver.execute_script(
                "arguments[0].click();",
                build_periodically
            )

        self.wait10.until(
            EC.element_to_be_selected(build_periodically)
        )

        return self

    def enter_build_periodically_schedule(
            self, schedule: str
    ) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.visibility_of_element_located(self.BUILD_PERIODICALLY_SCHEDULE)
        ).send_keys(schedule)

        return self

    def is_build_periodically_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.BUILD_PERIODICALLY)
        ).is_selected()

    def get_build_periodically_schedule(self) -> str:
        return self.wait10.until(
            EC.visibility_of_element_located(self.BUILD_PERIODICALLY_SCHEDULE)
        ).get_attribute("value") or ""

    def enable_poll_scm(self) -> FreestyleConfigurationPage:
        poll_scm_label = self.wait10.until(
            EC.presence_of_element_located(self.POLL_SCM_LABEL)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            poll_scm_label
        )

        poll_scm = self.wait10.until(
            EC.presence_of_element_located(self.POLL_SCM)
        )

        self.wait10.until(
            EC.element_to_be_selected(poll_scm)
        )

        return self

    def enter_poll_scm_schedule(
            self, schedule: str
    ) -> FreestyleConfigurationPage:
        self.wait10.until(
            EC.visibility_of_element_located(self.POLL_SCM_SCHEDULE)
        ).send_keys(schedule)

        return self

    def is_poll_scm_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.POLL_SCM)
        ).is_selected()

    def get_poll_scm_schedule(self) -> str:
        return (
                self.wait10.until(
                    EC.visibility_of_element_located(self.POLL_SCM_SCHEDULE)
                ).get_attribute("value") or ""
        )

    def enable_build_after_projects(self) -> FreestyleConfigurationPage:
        build_after_projects = self.wait10.until(
            EC.presence_of_element_located(self.BUILD_AFTER_PROJECTS)
        )

        if not build_after_projects.is_selected():
            build_after_projects_label = self.wait10.until(
                EC.presence_of_element_located(self.BUILD_AFTER_PROJECTS_LABEL)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                build_after_projects_label
            )

        self.wait10.until(
            EC.element_to_be_selected(build_after_projects)
        )

        return self

    def is_build_after_projects_selected(self) -> bool:
        return self.wait10.until(
            EC.visibility_of_element_located(self.BUILD_AFTER_PROJECTS)
        ).is_selected()

    def are_projects_to_watch_available(self) -> bool:
        projects_to_watch = self.wait10.until(
            EC.visibility_of_element_located(self.PROJECTS_TO_WATCH)
        )

        return projects_to_watch.is_displayed() and projects_to_watch.is_enabled()

    def is_success_threshold_selected(self) -> bool:
        return self.wait10.until(
            EC.presence_of_element_located(self.SUCCESS_THRESHOLD)
        ).is_selected()

    def are_other_thresholds_displayed(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
            for locator in [
                self.UNSTABLE_THRESHOLD,
                self.FAILURE_THRESHOLD,
                self.ABORTED_THRESHOLD,
            ]
        )

    def are_build_trigger_helper_tooltips_correct(self) -> bool:
        jenkins_url = self.driver.current_url.split("/job/")[0]

        help_items = [
            (
                self.BUILD_PERIODICALLY_HELP,
                "Provides a cron -like feature to periodically execute this project."
            ),
            (
                self.POLL_SCM_HELP,
                "Configure Jenkins to poll changes in SCM."
            ),
            (
                self.BUILD_AFTER_PROJECTS_HELP,
                "Set up a trigger so that when some other projects finish building, a new build is scheduled for this project."
            ),
        ]

        help_urls = []

        for locator, expected_text in help_items:
            help_element = self.wait10.until(
                EC.presence_of_element_located(locator)
            )
            help_urls.append(
                (help_element.get_attribute("helpurl"), expected_text)
            )

        help_results = []

        for help_url, expected_text in help_urls:
            self.driver.get(jenkins_url + help_url)

            help_text = self.wait10.until(
                EC.visibility_of_element_located((By.TAG_NAME, "body"))
            ).text

            help_results.append(expected_text in help_text)

        return all(help_results)

    def click_post_build_actions(self):
        self.wait10.until(
            EC.element_to_be_clickable(self.POST_BUILD_ACTIONS_BUTTON)
        ).click()

        return self

    def get_available_post_build_actions(self) -> list[str]:
        self.wait10.until(
            EC.presence_of_all_elements_located(self.POST_BUILD_ACTION_ITEMS)
        )

        return [
            item.get_attribute("textContent").strip()
            for item in self.driver.find_elements(*self.POST_BUILD_ACTION_ITEMS)
        ]

    def click_add_post_build_action(self):
        add_button = self.driver.find_element(
            *self.ADD_POST_BUILD_ACTION_BUTTON
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'start'});",
            add_button
        )
        self.driver.execute_script("window.scrollBy(0, 250);")

        add_button = self.wait10.until(
            EC.element_to_be_clickable(self.ADD_POST_BUILD_ACTION_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].click();",
            add_button
        )
        return self

    def select_post_build_action(self, action):
        action_locator = (
            By.XPATH,
            f"//button[contains(@class, 'jenkins-dropdown__item') and normalize-space()='{action}']"
        )
        self.wait10.until(
            EC.element_to_be_clickable(action_locator)
        ).click()
        return self

    def add_post_build_actions(self, actions):
        for action in actions:
            self.click_add_post_build_action()
            self.select_post_build_action(action)
        return self

    def are_save_apply_buttons_available(self) -> bool:
        return all(
            self.wait10.until(
                EC.visibility_of_element_located(locator)
            ).is_enabled()
            for locator in [self.SAVE_BUTTON, self.APPLY_BUTTON]
        )