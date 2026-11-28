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

def test_discard_old_builds_saves_days_and_max_builds(browser):
    item_name = "DiscardOldBuildsTestItem"
    days_to_keep = "5"
    max_builds_to_keep = "10"

    configuration_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(item_name)
        .select_freestyle_and_click_ok()
        .enable_discard_old_builds()
        .enter_days_to_keep_builds(days_to_keep)
        .enter_max_builds_to_keep(max_builds_to_keep)
    )

    configuration_page.click_save()

    reopened_configuration_page = (
        configuration_page
        .goto_home_page()
        .click_project(item_name)
        .click_configuration()
    )

    assert reopened_configuration_page.get_days_to_keep_builds() == days_to_keep
    assert reopened_configuration_page.get_max_builds_to_keep() == max_builds_to_keep
