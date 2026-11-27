import time

from pages.footer_page import Footer


def test_jenkins_version(browser):
    footer = Footer(browser)

    assert footer.is_footer_displayed()
    assert footer.get_jenkins_version() == "Jenkins 2.580.1"


def test_version_dropdown_items(browser):
    items = (
        Footer(browser)
        .click_jenkins_version()
        .get_version_dropdown_items()
    )

    assert items == ["About Jenkins", "Get involved", "Website"]


def test_about_jenkins(browser):
    about_page = (
        Footer(browser)
        .click_about_jenkins()
    )

    assert "/about/" in browser.current_url
    assert about_page.get_header_text() == "Jenkins"


def test_get_involved_link(browser):
    external_page = (
        Footer(browser)
        .click_get_involved()
    )

    assert "jenkins.io/participate" in browser.current_url
    assert external_page.get_header_text() == "Participate and Contribute"


def test_website_link(browser):
    external_page = (
        Footer(browser)
        .click_website()
    )

    assert "jenkins.io" in browser.current_url
    assert external_page.get_header_text() == "Jenkins"


def test_footer_rest_api_link(browser):
    rest_api_page = (
        Footer(browser)
        .click_rest_api()
    )

    assert "/api/" in browser.current_url
    assert rest_api_page.get_header_text() == "REST API"
