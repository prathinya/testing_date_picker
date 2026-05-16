import logging

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://formy-project.herokuapp.com/datepicker"

WAIT_TIME = 5

TEST_DATES = [
    "05/02/2026",
    "10/15/2027",
    "12/25/2028"
]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatePickerPage:

    DATE_PICKER_INPUT = (By.ID, "datepicker")

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            WAIT_TIME
        )

    def open_page(self):

        self.driver.get(BASE_URL)

        logging.info(
            "Datepicker page opened successfully."
        )

    def enter_date(self, date_value):

        date_field = self.wait.until(
            ec.element_to_be_clickable(
                self.DATE_PICKER_INPUT
            )
        )

        date_field.clear()

        date_field.send_keys(date_value)

        date_field.send_keys("\n")

        logging.info(
            "Date entered successfully -> %s",
            date_value
        )

    def get_selected_date(self):

        date_field = self.wait.until(
            ec.presence_of_element_located(
                self.DATE_PICKER_INPUT
            )
        )

        return date_field.get_attribute(
            "value"
        )


def initialize_browser():

    chrome_options = Options()

    chrome_options.add_argument(
        "--start-maximized"
    )

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver


@pytest.fixture
def driver():

    driver = initialize_browser()

    yield driver

    driver.quit()

    logging.info(
        "Browser closed successfully."
    )


@pytest.mark.parametrize(
    "expected_date",
    TEST_DATES
)
def test_datepicker(
    driver,
    expected_date
):

    datepicker_page = DatePickerPage(
        driver
    )

    datepicker_page.open_page()

    datepicker_page.enter_date(
        expected_date
    )

    selected_date = (
        datepicker_page.get_selected_date()
    )

    assert (
        selected_date == expected_date
    ), (
        f"Expected '{expected_date}' "
        f"but got '{selected_date}'"
    )

    logging.info(
        "TEST PASSED: Date selected successfully."
    )


if __name__ == "__main__":

    pytest.main(
        ["-v"]
    )
