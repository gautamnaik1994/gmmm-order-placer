import httpx
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
        headers = {
            "Authorization": token
        }
        # todays_orders = trade_signals_table.query(KeyConditionExpression=Key('pk').eq(
        #     f"{todays_date}#00:00") & Key('sk').begins_with(f"long#{current_hour}:00"))["Items"]
        response = httpx.get(
            f"{os.environ['API_ROOT']}/signals/{date_time_helpers.get_current_date()}?strategy=long#{current_hour}:00", headers=headers)

        if response.status_code != 200:
            logging.error(
                f'Failed to fetch signals \n ``` {response.text}```')
            raise Exception("Failed to fetch signals")

        response = response.json()
        if len(response["data"]) == 0:
            send_telegram.t_error('No signals found in signals')
            raise Exception("No signals found in signals")
        for item in response["data"]:
            signals.append({
                "symbol": item["symbol"],
                "price": item["price"],
                "transaction_type": -1 if item["transaction_type"] == "S" else 1,
                "token": item["more"]["token"]
            })
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
    creds_path = Path(__file__).resolve().parent / "creds.json"
    signals_path = Path(__file__).resolve().parent / "signals.json"

    with creds_path.open() as f:
        data = json.load(f)
        token = data["s_token"]
    signals = []
    todays_date = date_time_helpers.get_current_date()
    current_hour = datetime.now().strftime("%H")
    try:
        headers = {
            "Authorization": token
        }
        response = httpx.get(
            f"{os.environ['API_ROOT']}/signals/{date_time_helpers.get_current_date()}?strategy=long#{current_hour}:00", headers=headers)

        if response.status_code != 200:
            logging.error(
                f'Failed to fetch signals \n ``` {response.text}```')
            raise Exception("Failed to fetch signals")

        response = response.json()
        if len(response["data"]) == 0:
            send_telegram.t_error('No signals found in signals')
            raise Exception("No signals found in signals")
        for item in response["data"]:
            signals.append({
                "symbol": item["symbol"],
                "price": item["price"],
                "transaction_type": -1 if item["transaction_type"] == "S" else 1,
                "token": item["more"]["token"]
            })
        signals_path.write_text(json.dumps(signals))
        send_telegram.t_success('Signals fetched successfully.')
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
    try:
        fyers_api.direct_place_order_process(
                signals, 5000)
        send_telegram.t_success('Orders placed successfully.')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Failed to place orders \n ``` {e}```')



