import csv
import requests


def update_rates(out_filename, include_all_dates=True):
    """
    Downloads exchange rates, by default from the Code for IATI
    IMF Exchange Rates mirror:
    https://codeforiati.org/imf-exchangerates/imf_exchangerates.csv
    """
    url = 'https://codeforiati.org/imf-exchangerates/imf_exchangerates.csv'
    req = requests.get(url)

    with open(out_filename, 'w') as f:
        f.write(req.text)


if __name__ == "__main__":
    update_rates('data/consolidated_rates.csv')
