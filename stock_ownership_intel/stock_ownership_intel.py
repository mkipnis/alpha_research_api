import json
import os
import time
import requests


def print_holdings_columns(data, key=None):
    dates = sorted(
        {d for dates in data.values() for d in dates},
        reverse=True
    )

    col_width = 14
    name_width = max(len(k) for k in data) + 2

    # Header
    header = f"{'Institution'.ljust(name_width)}"
    for d in dates:
        header += d.rjust(col_width)
    print(header)
    print("-" * len(header))

    # Rows
    for inst, inst_dates in data.items():
        row = inst.ljust(name_width)
        for d in dates:
            val = inst_dates.get(d)
            if key is not None:
                cell = f"{int(val['value']):,}" if val else "—"
            else:
                cell = f"{int(float(val)):,}" if val else "—"
            row += cell.rjust(col_width)
        print(row)

if __name__ == "__main__":

    # Your x-rapidapi-key
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_URL = os.getenv(
        "RAPID_API_URL",
        "https://stock-ownership-intel.p.rapidapi.com/"
    )

    if not RAPID_API_KEY:
        raise RuntimeError("RAPID_API_KEY environment variable is not set")

    payload = {}
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "X-RapidAPI-Host": "stock-ownership-intel.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    #################################### Filing Dates ############################################
    print("\nRetrieving filing dates...")
    time.sleep(1)
    response = requests.post(url=RAPID_API_URL + "/filing_dates/", json=payload, headers=headers)
    filing_dates = response.json()
    print(filing_dates)

    #################################### Institutions ############################################
    print("\nRetrieving Institutions...")
    time.sleep(1)
    response = requests.post(url=RAPID_API_URL + "/institutions/", json=payload, headers=headers)
    institutions = response.json()
    print(f"Number of Institutions - {len(institutions)}")

    #################################### Securities ############################################
    print("\nRetrieving Securities...")
    time.sleep(1)
    response = requests.post(url=RAPID_API_URL + "/securities/", json=payload, headers=headers)
    securities = response.json()
    print(f"Number of Securities - {len(securities)}")

    # Returns the equity holdings disclosed by a specific institutional investment manager in its SEC Form 13F filings, providing a quarterly snapshot of the institution’s reported portfolio.
    print("\nRetrieving holdings for institution...")
    time.sleep(1)
    payload['institution'] = 'Bridgewater Advisors Inc.'
    response = requests.post(url=RAPID_API_URL + "/holdings_for_institution/", json=payload, headers=headers)
    securities_for_institution = response.json()
    print_holdings_columns(securities_for_institution, key='value')

    # Retrieves a list of institutional investment managers that have reported holdings of a specified security in their SEC Form 13F filings.
    # Each institution entry includes details such as the filing manager, reported position size, and market value for the security.
    print("\nRetrieving holders of security...")
    time.sleep(1)
    payload['symbol']='AAPL'
    response = requests.post(url=RAPID_API_URL + "/holders_of_security/", json=payload, headers=headers)
    holders_of_security = response.json()
    print_holdings_columns(holders_of_security, key='value')

    # Equity holdings reported in SEC Form 13F filings for a specific institutional manager, limited to companies classified within a given sector.
    print("\nRetrieving holdings for institution and sector...")
    time.sleep(1)
    payload['institution'] = 'Bridgewater Advisors Inc.'
    payload['sector'] = 'Technology Services'
    response = requests.post(url=RAPID_API_URL + "/holdings_for_institution_and_sector/", json=payload, headers=headers)
    holdings_for_institution_and_sector = response.json()
    print_holdings_columns(holdings_for_institution_and_sector, key='value')

    # Equity holdings reported in SEC Form 13F filings for a specific institutional manager, limited to companies classified within a given industry.
    print("\nRetrieving holdings for institution and industry...")
    time.sleep(1)
    payload['institution'] = 'Bridgewater Advisors Inc.'
    payload['industry'] = 'Packaged Software'
    response = requests.post(url=RAPID_API_URL + "/holdings_for_institution_and_industry/", json=payload, headers=headers)
    holdings_for_institution_and_industry = response.json()
    print_holdings_columns(holdings_for_institution_and_industry, key='value')

    # The aggregated market value of all SEC Form 13F–reported holdings for companies within a specified sector, based on quarter-end filing data.
    print("\nRetrieving holdings for sector...")
    time.sleep(1)
    payload['sector'] = 'Technology Services'
    response = requests.post(url=RAPID_API_URL + "/holdings_for_sector/", json=payload, headers=headers)
    holdings_for_sector = response.json()
    print_holdings_columns(holdings_for_sector)

    # The aggregated market value of all SEC Form 13F–reported holdings for companies within a specified industry, based on quarter-end filing data.
    print("\nRetrieving holdings for industry...")
    time.sleep(1)
    payload['industry'] = 'Packaged Software'
    response = requests.post(url=RAPID_API_URL + "/holdings_for_industry/", json=payload, headers=headers)
    holdings_for_industry = response.json()
    print_holdings_columns(holdings_for_industry)