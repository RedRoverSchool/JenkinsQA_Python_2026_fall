from pages.home_page import HomePage


def test_dropdown_shows_matching_existing_items(browser):
    main_freestyle_project_name = "First Job"

    dropdown_value_list = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(main_freestyle_project_name)
        .select_freestyle_and_click_ok()
        .click_save()
        .goto_home_page()
        .click_new_item()
        .click_duplicate_option()
        .set_duplicate_item_name(main_freestyle_project_name)
        .get_duplicate_item_names()
    )

    assert main_freestyle_project_name in dropdown_value_list


def test_dropdown_shows_no_items_for_non_matching_value(browser):
    main_freestyle_project_name = "First Job"
    non_existing_name = "Nonexisting"

    no_items_message = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(main_freestyle_project_name)
        .select_freestyle_and_click_ok()
        .click_save()
        .goto_home_page()
        .click_new_item()
        .click_duplicate_option()
        .set_duplicate_item_name(non_existing_name)
        .get_no_items_alert_message()
    )

    assert no_items_message == "No items"


def test_error_on_non_existed_item(browser):
    main_freestyle_project_name = "First Job"
    non_existing_name = "Nonexisting"

    error_page = (
        HomePage(browser)
        .click_new_item()
        .set_item_name(main_freestyle_project_name)
        .select_freestyle_and_click_ok()
        .click_save()
        .goto_home_page()
        .click_new_item()
        .set_item_name(non_existing_name)
        .click_duplicate_option()
        .set_duplicate_item_name(non_existing_name)
        .click_ok_expecting_error()
    )

    assert error_page.get_error_header() == "Error"
    assert error_page.get_error_message() == f"No such job: {non_existing_name}"

    home_page = error_page.goto_home_page()

    assert home_page.is_project_displayed(main_freestyle_project_name)
    assert home_page.is_project_absent(non_existing_name)