# Copyright (c) Mike Kipnis (mike.kipnis@gmail.com) - Alpha Research Online

import json
import os
import time
import requests

RAPID_API_URL = "https://us-treasuries.p.rapidapi.com"

if __name__ == "__main__":

    # Your x-rapidapi-key
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_URL = os.getenv(
        "RAPID_API_URL",
        "https://us-treasuries.p.rapidapi.com"
    )

    if not RAPID_API_KEY:
        raise RuntimeError("RAPID_API_KEY environment variable is not set")

    payload = {}
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "X-RapidAPI-Host": "us-treasuries.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    #################################### Latest Key Rates ############################################
    print("\nRetrieving Latest Key Rates ...")
    time.sleep(2)
    response = requests.post(url=RAPID_API_URL + "/key_rates/", json=payload, headers=headers)
    latest_key_rates = response.json()
    print(json.dumps(latest_key_rates, indent=4))

    #################################### Historical Key Rates #########################################
    print("\nRetrieving Historical Key Rates ...")
    time.sleep(2)

    payload = {'start_date': '2022-01-01', 'end_date': '2022-02-01'}
    response = requests.post(url=RAPID_API_URL + "/key_rates/", json=payload, headers=headers)
    print(json.dumps(response.json(), indent=4))

    #################################### Instruments ##################################################
    print("\nRetrieving Available Instruments ...")
    time.sleep(3)

    url_instruments = RAPID_API_URL + "/instruments/"
    response = requests.post(url_instruments, json=payload, headers=headers)
    print(json.dumps(response.json(), indent=4))

    cusips_to_price = list(response.json()['instruments'].keys())

    #################################### Pricing Request ##################################################
    business_date = next(iter(latest_key_rates['key_rates'].keys()))
    payload = {"business_date": business_date,
               "yield_curve": latest_key_rates['key_rates'][business_date],
               #"instruments": ["912810FM5", "912810TR9"]}
               "instruments": cusips_to_price } # all available instruments
    print(json.dumps(payload, indent=4))
    token_response = requests.post(url=RAPID_API_URL + "/curve_price_request/", json=payload, headers=headers)

    print("\nSubmitting Pricing Request ...")
    time.sleep(3)

    print(json.dumps(token_response.json(), indent=4))

    #################################### Pricing Response ##################################################
    print("\nRetrieving Pricing Request ...")
    time.sleep(3)

    pricer_response = requests.post(url=RAPID_API_URL + "/curve_price_results/", json=token_response.json(),
                                    headers=headers)
    print(json.dumps(pricer_response.json(), indent=4))

    exit(0)
