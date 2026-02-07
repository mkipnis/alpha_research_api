import json
import os
import time
import requests


def pretty_print_stocks(data):
    if not data:
        print("(no data)")
        return

    columns = ["symbol", "name", "sector", "industry"]

    # Normalize values and compute column widths
    rows = []
    widths = {col: len(col) for col in columns}

    for item in data:
        row = {}
        for col in columns:
            val = item.get(col)
            text = "" if val is None else str(val)
            row[col] = text
            widths[col] = max(widths[col], len(text))
        rows.append(row)

    # Helpers
    def sep():
        return "+".join("-" * (widths[c] + 2) for c in columns)

    def fmt(row):
        return " | ".join(row[c].ljust(widths[c]) for c in columns)

    # Print table
    print(fmt({c: c.upper() for c in columns}))
    print(sep())
    for row in rows:
        print(fmt(row))


def pretty_print_vol_data(vol_data):
    for date, data in vol_data.items():
        print(f"Date: {date}")
        if 'underlying_price' in data:
            print(f"  Underlying Price: {data['underlying_price']:.2f}")
            vols = data.get('volatility', {})
        else:
            vols = data

        for exp_date, exp_data in vols.items():
            print(f"  Expiration: {exp_date}")
            calls = exp_data.get('calls', {})
            puts = exp_data.get('puts', {})

            if calls:
                print("    Calls:")
                for strike, value in sorted(calls.items(), key=lambda x: float(x[0])):
                    print(f"      {strike:>7}: {value:>7.3f}")

            if puts:
                print("    Puts:")
                for strike, value in sorted(puts.items(), key=lambda x: float(x[0])):
                    print(f"      {strike:>7}: {value:>7.3f}")
        print()  # blank line between dates


if __name__ == "__main__":

    # Your x-rapidapi-key
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_URL = os.getenv(
        "RAPID_API_URL",
        "https://volatlityhub.p.rapidapi.com/"
    )

    if not RAPID_API_KEY:
        raise RuntimeError("RAPID_API_KEY environment variable is not set")

    payload = {}
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "X-RapidAPI-Host": "volatlityhub.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    print("\nRetrieving underlying symbols...")
    time.sleep(1)
    response = requests.post(url=RAPID_API_URL + "/underlying_symbols/", json=payload, headers=headers)
    underlying_symbols = response.json()
    print(underlying_symbols)
    pretty_print_stocks(underlying_symbols)

    print("\nRetrieving latest vols...")
    time.sleep(1)
    payload['underlying_symbol'] = 'AAPL'
    response = requests.post(url=RAPID_API_URL + "/volatility/", json=payload, headers=headers)
    underlying_symbols = response.json()
    pretty_print_vol_data(underlying_symbols)

    print("\nRetrieving vols... 2026-01-01 - 2026-01-25")
    time.sleep(1)
    payload['underlying_symbol'] = 'AAPL'
    payload['start_date'] = '2026-01-01'
    payload['end_date'] = '2026-01-25'
    response = requests.post(url=RAPID_API_URL + "/volatility/", json=payload, headers=headers)
    underlying_symbols = response.json()
    pretty_print_vol_data(underlying_symbols)

    print("\nRetrieving vols... from 2026-01-01")
    time.sleep(1)
    payload['underlying_symbol'] = 'AAPL'
    payload['start_date'] = '2026-01-01'
    response = requests.post(url=RAPID_API_URL + "/volatility/", json=payload, headers=headers)
    underlying_symbols = response.json()
    pretty_print_vol_data(underlying_symbols)

    print("\nRetrieving vol hub data...")
    time.sleep(1)
    response = requests.post(url=RAPID_API_URL + "/vol_snapshot/", json=payload, headers=headers)
    vol_snapshot = response.json()
    print(vol_snapshot)
