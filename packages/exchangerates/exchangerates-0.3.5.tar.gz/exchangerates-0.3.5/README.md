A module to make it easier to handle historical exchange rates.

Since version 0.3.5, rates are downloaded from a separate scraper hosted by Code for IATI. You can find the code for that scraper on Github:
https://github.com/codeforiati/imf-exchangerates

The data from that scraper is made available here:
https://codeforiati.org/imf-exchangerates/imf_exchangerates.csv

## Instructions

Install from PyPI:

    pip install exchangerates

Create a CurrencyConverter object:

    import exchangerates
    converter = exchangerates.CurrencyConverter(update=True)

Note: `update=True` will lead to fresh exchange rates being downloaded.

## Usage

Get a list of the available currencies:

    print converter.known_currencies()

Get the conversion rate for a specific currency and date:

    print converter.closest_rate("USD", datetime.date(2012,7,20))
    print converter.closest_rate("EUR", datetime.date(2014,7,20))
    print converter.closest_rate("EUR", datetime.date(2014,7,20))

You can also just generate a consolidated file of exchange rates:

    python get_rates.py

Result will be at `data/consolidated_rates.csv`.
