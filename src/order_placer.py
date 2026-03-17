import argparse

import requests
import boto3
import send_telegram as send_telegram
import logging
import json
import os
from dotenv import load_dotenv
import date_time_helpers as date_time_helpers
from datetime import datetime
import fyers_api
from pathlib import Path
from aws_setup import _sigv4_signed_headers


load_dotenv()


def fetch_and_place_orders():
    creds_path = Path(__file__).resolve().parent / "creds.json"
    signals_path = Path(__file__).resolve().parent / "signals.json"

    with creds_path.open() as f:
        data = json.load(f)
        token = data["s_token"]
    signals = []
    todays_date = date_time_helpers.get_current_date()
    current_hour = datetime.now().strftime("%H")
    try:
        url= f"{os.environ['API_ROOT']}/signals/{todays_date}?strategy=long#{current_hour}:00"
        logging.info(f"Fetching signals from {url}")

        headers = _sigv4_signed_headers(url)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(
                f'Failed to fetch signals \n ``` {response.text}```')
            raise Exception("Failed to fetch signals")

        logging.info(f"Signals fetched successfully: {response.json()}")
        response = response.json()
        if len(response["data"]) == 0:
            send_telegram.t_error('No signals found in signals')
            raise Exception("No signals found in signals")
        for item in response["data"]:
            signals.append(item)
        fyers_api.direct_place_order_process(
                response["data"], 5000)
        signals_path.write_text(json.dumps(signals))
        send_telegram.t_success('Signals fetched successfully.')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Failed to fetch signals \n ``` {e}```')
        
# separate  above code into two functions - one for fetching signals and storing in json, another for placing orders using fyers api

def fetch_orders():
    signals_path = Path(__file__).resolve().parent / "signals.json"
    signals_path.write_text(json.dumps([]))
    signals = []
    current_hour = datetime.now().strftime("%H")
    todays_date = date_time_helpers.get_current_date()
    try:
        url = f"{os.environ['API_ROOT']}/signals/{todays_date}?strategy=long#{current_hour}:00"
        logging.info(f"Fetching signals from {url}")
        headers = _sigv4_signed_headers(url)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(
                f'Failed to fetch signals \n ``` {response.text}```')
            raise Exception("Failed to fetch signals")

        response = response.json()
        logging.info(f"Signals fetched successfully: {response}")
        if len(response["data"]) == 0:
            send_telegram.t_error('No signals found in signals')
            raise Exception("No signals found in signals")
        for item in response["data"]:
            signals.append(item)
        signals_path.write_text(json.dumps(signals))
        symbols = [signal["symbol"] for signal in signals]
        send_telegram.t_success(f'Signals fetched successfully for symbols: {", ".join(symbols)}')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Failed to fetch signals \n ``` {e}```')
        

def place_orders():
    signals_path = Path(__file__).resolve().parent / "signals.json"
    if not signals_path.exists():
        send_telegram.t_error('Signals file not found')
        raise Exception("Signals file not found")
    signals = json.loads(signals_path.read_text())

    # check if signals are empty
    if len(signals) == 0:
        send_telegram.t_error('No signals found in signals file')
        raise Exception("No signals found in signals file")

    try:
        fyers_api.direct_place_order_process(
                signals, 5000)
        send_telegram.t_success('Orders placed successfully.')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Failed to place orders \n ``` {e}```')


if __name__ == "__main__":
    # read args to decide whether to fetch orders or place orders or both


    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true", help="Fetch orders")
    parser.add_argument("--place", action="store_true", help="Place orders")
    args = parser.parse_args()
    if args.fetch:
        fetch_orders()
    if args.place:
        place_orders()
    else:
        fetch_orders()
        place_orders()


