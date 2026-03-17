import requests
import boto3
import send_telegram as send_telegram
import logging
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from aws_setup import _sigv4_signed_headers


load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", "DEV")



def decode(cipher, key):
    cipher = bytes(cipher.encode('utf-8'))
    reps = (len(cipher)-1)//len(key) + 1
    key = (key * reps)[:len(cipher)].encode('utf-8')
    clear = bytes(i1 ^ i2 for (i1, i2) in zip(cipher, key))
    return clear.decode('utf-8')


def fyers_login():
    creds_path = Path(__file__).resolve().parent / "creds.json"
    try:
        url = f"{os.environ['API_ROOT']}/dangerous/time"
        signed_headers = _sigv4_signed_headers(url)
        response = requests.get(url, headers=signed_headers)
        response = response.json()
        f_token = decode(response, os.environ["GEN_PASS_KEY"])
        # with open("creds.json", "w") as outfile:
        #     outfile.write(json.dumps({
        #         'pk': "BROKER",
        #         'sk': 'FYERS',
        #         'value': f_token,
        #         'more': {
        #             'api_key': os.environ["FYERS_API_KEY"],
        #         },

        #     }))
        creds_path.write_text(json.dumps({
            'pk': "BROKER",
            'sk': 'FYERS',
            'value': f_token,
            'more': {
                'api_key': os.environ["FYERS_API_KEY"],
            },

        }))
        send_telegram.t_success('Fyers token fetched successfully.')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Fyers token fetch failed \n ``` {e}```')


if __name__ == '__main__':
    fyers_login()
