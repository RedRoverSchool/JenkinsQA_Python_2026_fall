import re
from pages.home_page import HomePage
import pytest
from pages.pipeline_configuration_page import PipelineConfigurationPage

PIPELINE_NAME = "Pipeline 1"
QP_POSITIVE = "10"
QP_NEGATIVE = "-2"
NON_INTEGER = "5.5"
NEGATIVE_ERROR = "This value should be larger than 0"
NON_INTEGER_ERROR = "Not an integer"


def test_quiet_period_accepts_positive_integer(browser):
    quiet_period_seconds = (
        create_pipeline(browser)
        .click_on_left_side_section(PipelineConfigurationPage.ClickOnLeftSideSection.ADVANCED)
        .open_advanced_dropdown()
        .set_quiet_period(QP_POSITIVE)
        .click_save()
        .open_configuration_pipeline_page()
        .click_on_left_side_section(PipelineConfigurationPage.ClickOnLeftSideSection.ADVANCED)
        .open_advanced_dropdown()
        .get_quiet_period()
    )

    assert quiet_period_seconds == QP_POSITIVE


@pytest.mark.parametrize("value,expected_error", [
    pytest.param(QP_NEGATIVE, NEGATIVE_ERROR, id="negative_integer_value"),
    pytest.param(NON_INTEGER, NON_INTEGER_ERROR, id="non_integer_value"),
])
def test_quiet_period_rejects_negative_and_non_integer_values(browser, value, expected_error):
    error = (
        create_pipeline(browser)
        .click_on_left_side_section(PipelineConfigurationPage.ClickOnLeftSideSection.ADVANCED)
        .open_advanced_dropdown()
        .set_quiet_period(value)
        .get_quiet_period_error()
    )

    assert error == expected_error


@pytest.mark.parametrize("value", [
    pytest.param("AbCdeEГд", id="letters_as_value"),
    pytest.param("!@#$%^&*()", id="symbols_as_value"),
    pytest.param("A512@d", id="mix_value"),
])
def test_quiet_period_letters_and_symbols_can_not_be_entered(browser, value):
    input_field = (
        create_pipeline(browser)
        .click_on_left_side_section(PipelineConfigurationPage.ClickOnLeftSideSection.ADVANCED)
        .open_advanced_dropdown()
        .set_quiet_period(value)
        .get_quiet_period()
    )

    input_expected = re.sub(r"[^0-9]", "", value)

    assert input_field == input_expected


def create_pipeline(browser):
    return (
        HomePage(browser)
        .click_new_item()
        .set_item_name(PIPELINE_NAME)
        .select_pipeline_and_click_ok()
    )
