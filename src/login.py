import httpx
import requests
import boto3
import send_telegram as send_telegram
import logging
import json
import os
from dotenv import load_dotenv
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", "DEV")


# def aws_login():

#     if ENVIRONMENT == "DEV":

#         client = boto3.client('cognito-idp',
#                             #   region_name="ap-south-1",
#                             #   aws_access_key_id=os.environ["ACCESS_KEY_ID"],
#                             #   aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"]
#                               )
#     else:

#         # 1. Create a session using your specific Roles Anywhere profile
#         # This automatically triggers the credential_process (aws_signing_helper)
#         session = boto3.Session(profile_name='roles-anywhere')

#         # 2. Initialize the client from that session
#         client = session.client('cognito-idp', region_name="ap-south-1")

#     response = client.admin_initiate_auth(
#         ClientId=os.environ["CLIENT_ID"],
#         AuthFlow='ADMIN_USER_PASSWORD_AUTH',
#         UserPoolId=os.environ["USER_POOL_ID"],
#         AuthParameters={
#             'USERNAME': os.environ["USERNAME"],
#             'PASSWORD': os.environ["PASSWORD"]
#         }
#     )
#     print("AWS login successful!", response['AuthenticationResult']['AccessToken'])
#     return response['AuthenticationResult']['AccessToken']


def decode(cipher, key):
    cipher = bytes(cipher.encode('utf-8'))
    reps = (len(cipher)-1)//len(key) + 1
    key = (key * reps)[:len(cipher)].encode('utf-8')
    clear = bytes(i1 ^ i2 for (i1, i2) in zip(cipher, key))
    return clear.decode('utf-8')




def test_local_api():
    session = boto3.Session(profile_name='roles-anywhere') #
    credentials = session.get_credentials()
    region = session.region_name or "ap-south-1"
    
    url = f"{os.environ['API_ROOT']}/dangerous/time"
    
    # 1. Create the request object
    # It is important to match the method and URL exactly
    request = AWSRequest(method='GET', url=url)
    
    # 2. Sign the request
    # This adds 'Authorization', 'X-Amz-Date', and 'X-Amz-Security-Token' to request.headers
    signer = SigV4Auth(credentials, 'execute-api', region)
    signer.add_auth(request)
    
    # 3. PREPARE THE HEADERS
    # We must convert the botocore CaseInsensitiveDict to a plain dict
    signed_headers = dict(request.headers.items())
    
    # 4. Execute with requests
    # NOTE: We use the signed headers and avoid letting 'requests' add extras if possible
    response = requests.get(url, headers=signed_headers)
    
    print(f"Status: {response.status_code}")
    try:
        print(f"Body: {response.json()}")
    except:
        print(f"Raw Body: {response.text}")

test_local_api()





def fyers_login():
    try:
        session = boto3.Session(profile_name='roles-anywhere') 
        credentials = session.get_credentials()
        region = session.region_name or "ap-south-1"
        url = f"{os.environ['API_ROOT']}/dangerous/time"
        request = AWSRequest(method='GET', url=url)
        signer = SigV4Auth(credentials, 'execute-api', region)
        signer.add_auth(request)
        signed_headers = dict(request.headers.items())
        response = requests.get(url, headers=signed_headers)
        response = response.json()
        f_token = decode(response, os.environ["GEN_PASS_KEY"])
        with open("creds.json", "w") as outfile:
            outfile.write(json.dumps({
                'pk': "BROKER",
                'sk': 'FYERS',
                'value': f_token,
                'more': {
                    'api_key': os.environ.get('FYERS_UID', ''),
                },

            }))
        send_telegram.t_success('Fyers token fetched successfully.')
    except Exception as e:
        logging.error(e)
        send_telegram.t_error(
            f'Fyers token fetch failed \n ``` {e}```')


if __name__ == '__main__':
    fyers_login()
