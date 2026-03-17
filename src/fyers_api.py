import json
import date_time_helpers
import datetime as dt
import send_telegram
import time
import httpx
import urllib.parse
import logging
from pathlib import Path

fyers_api_base_url = 'https://api-t1.fyers.in/api/v3'

_CREDS_PATH = Path(__file__).resolve().parent / "creds.json"

access_token: str | None = None
api_key: str | None = None

headers: dict[str, str] | None = None
simple_headers: dict[str, str] | None = None


def _ensure_auth() -> None:
    global access_token, api_key, headers, simple_headers
    if headers is not None and simple_headers is not None:
        return

    try:
        raw = _CREDS_PATH.read_text().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Missing creds.json at {_CREDS_PATH}."
        ) from e

    if not raw:
        raise ValueError(f"{_CREDS_PATH} is empty.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {_CREDS_PATH}: {e}") from e

    access_token = data["value"]
    api_key = data["more"]["api_key"]

    headers = {
        'Authorization': f'{api_key}:{access_token}',
        'Content-Type': 'application/json'
    }
    simple_headers = {
        'Authorization': f'{api_key}:{access_token}',
    }

# TODO:create constants file
# TODO:create a function to get the order id


def chunkify(lst, chunk_size):
    nested = list(map(list, zip(*[iter(lst)]*chunk_size)))
    if rest := lst[len(lst) // chunk_size * chunk_size:]:
        nested.append(rest)
    return nested


def direct_place_order_process(order_data, per_script_limit):
    """
    This function will initiate the process of placing an order on fyers.com exactly at 9:15 AM
    """
    all_orders_obj = build_fyres_order_object(
        order_data, per_script_limit)
    if len(all_orders_obj) <= 10:
        place_order(all_orders_obj)
    else:
        all_orders_chunks = chunkify(all_orders_obj, 10)
        for chunk in all_orders_chunks:
            place_order(chunk)

    send_telegram.send_message(f"Fyers order placed successfully.")


def build_fyres_order_object(order_data, per_script_limit):
    # add offline order settings
    print("Building order object")
    all_orders = []
    for order in order_data:
        is_offline_order = order['more']['amo']
        quantity = int(int(per_script_limit)/order['price'])
        if quantity < 1 and order['transaction_type'] == 'B':
            continue
        _ = {
            "symbol": f"NSE:{order['symbol']}-EQ",
            "qty": int(order["quantity"]),
            "type": 2,
            "side": 1 if order['transaction_type'] == 'B' else -1,
            "productType": "CNC",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0 if is_offline_order else quantity,
            "offlineOrder": is_offline_order,
            "stopLoss": 0,
            "takeProfit": 0,
            "orderTag": order["strategy"].replace("_", "")
        }
        all_orders.append(_)
    return all_orders



def cancel_order(id: None):
    """
    Cancel an order on fyers.com
    """
    _ensure_auth()
    json_data = {
        'id': id,
    }
    cancel_order_api = f"{fyers_api_base_url}/orders/sync"
    response = httpx.delete(
        cancel_order_api, headers=headers, data=json.dumps(json_data))
    return response.json()


def exit_all_positions():
    """
    This function will exit the position on fyers.com
    """
    _ensure_auth()
    url = f"{fyers_api_base_url}/positions"
    data = {
        'exit_all': 1,
    }
    try:
        httpx.delete(
            url, headers=headers, data=json.dumps(data))
        # return response.json()
    except Exception as e:
        print(e)
        return None


def place_order(order_data):
    """
    Place an order on fyers.com
    """
    _ensure_auth()
    url = f"{fyers_api_base_url}/multi-order/sync"
    try:
        send_telegram.send_message(f"Placing order on fyers.com for {len(order_data)} orders.")
        # r = httpx.post(url, headers=headers, data=json.dumps(order_data))
        # return response.json()
    except Exception as e:
        print(e)
        send_telegram.send_message(f"Fyers order failed. Error: {e}")
        return None
    
def get_all_orders():
    """
    Get all orders on fyers.com
    """
    _ensure_auth()
    url = f"{fyers_api_base_url}/orders"
    try:
        response = httpx.get(url, headers=simple_headers)
        return response.json()
    except Exception as e:
        send_telegram.send_message(f"get_all_orders() failed. Error: {e}")
        print(e)
        return None


def square_off_all_orders():
    """
    This function will cancel all open orders on fyers.com
    """
    exit_all_positions()
    _placed_orders = get_all_orders()
    if _placed_orders is None:
        send_telegram.send_message(
            f"Could not fetch orders from fyers.com.")
        return None
    placed_orders = _placed_orders['orderBook']
    unexecuted_order = []
    for order in placed_orders:
        if order['message'] == 'CONFIRMED' or order['message'] == '':
            # print(order['symbol'])
            unexecuted_order.append({
                'id': order['id'],
            })
    if len(unexecuted_order) > 0:
        try:
            httpx.delete(f'{fyers_api_base_url}/orders-multi/sync',
                         headers=headers, data=json.dumps(unexecuted_order))
            send_telegram.send_message(f"Delete unexecuted orders api called")
        except Exception as e:
            print(e)
            send_telegram.send_message(
                f"Fyers oreder cancelletion failed: {e}")
            return None
    else:
        send_telegram.send_message(f"No open orders found.")
        return None
