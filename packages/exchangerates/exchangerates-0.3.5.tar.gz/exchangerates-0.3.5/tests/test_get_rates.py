import pathlib
import pytest
import csv
import datetime
import exchangerates


@pytest.fixture(scope="module")
def get_file():
    filename = 'test_data_exchangerates.csv'
    exchangerates.get_rates.update_rates(filename)
    yield filename
    pathlib.Path(filename).unlink()


@pytest.fixture()
def currency_converter(get_file):
    filename = get_file
    yield exchangerates.CurrencyConverter(
        update=False, source=filename)


def test_get_rates(get_file):
    filename = get_file
    with open(filename, 'r') as infile:
        csvreader = csv.DictReader(infile)
        assert csvreader.fieldnames == [
            'Date', 'Rate', 'Currency',
            'Frequency', 'Source',
            'Country code', 'Country']


def test_load_rates(currency_converter):#
    known_currencies = currency_converter.known_currencies()
    assert len(known_currencies) > 0


def test_closest_rate_usd(currency_converter):
    the_date = datetime.date(2024,1,1)
    closest_rate = currency_converter.closest_rate('USD',
        the_date)
    assert closest_rate['closest_date'] == the_date
    assert closest_rate['conversion_rate'] == 1


def test_closest_rate_eur(currency_converter):
    """
    Checks that the EUR rate is in 2024 and not 1:1
    """
    the_date = datetime.date(2024,7,1)
    closest_rate = currency_converter.closest_rate('EUR',
        the_date)
    assert closest_rate['closest_date'].year == the_date.year
    assert closest_rate['conversion_rate'] != 1


def test_rates_are_not_equal(currency_converter):
    """
    Checks that the EUR rate in 2024 is different
    from the EUR rate in 2014
    """
    date_1 = datetime.date(2024,7,1)
    closest_rate_1 = currency_converter.closest_rate('EUR',
        date_1)
    assert closest_rate_1['closest_date'].year == date_1.year
    date_2 = datetime.date(2014,7,1)
    closest_rate_2 = currency_converter.closest_rate('EUR',
        date_2)
    assert closest_rate_1['conversion_rate'] != closest_rate_2['conversion_rate']
