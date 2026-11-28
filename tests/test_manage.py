from pages.home_page import HomePage


def test_open_page(browser):
    manage_page = HomePage(browser).click_manage_jenkins()

    assert manage_page.get_page_title() == "Manage Jenkins"
    assert "System Configuration" in manage_page.get_group_names()
