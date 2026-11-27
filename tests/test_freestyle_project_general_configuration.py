from pages.home_page import HomePage

def test_general_section_ui_elements_and_defaults(browser):
    item_name = "GeneralSectionTestItem"

    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_freestyle_and_click_ok()
    )

    assert configuration_page.is_general_section_displayed()
    assert configuration_page.are_general_blocks_displayed()

    configuration_page.enable_discard_old_builds()
    strategy = configuration_page.get_discard_old_builds_strategy()

    assert strategy == "Log Rotation"
