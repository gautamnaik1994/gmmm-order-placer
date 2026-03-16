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


# Reuse a single session across functions/process lifetime.
# For SigV4 signing, we still freeze credentials per request to avoid using stale/expired values.
AWS_SESSION = boto3.Session(profile_name='roles-anywhere')


def _sigv4_signed_headers(url: str, method: str = 'GET', service: str = 'execute-api') -> dict:
    credentials = AWS_SESSION.get_credentials()
    if credentials is None:
        raise RuntimeError("Unable to load AWS credentials for profile 'roles-anywhere'.")

    frozen_credentials = credentials.get_frozen_credentials()
    region = AWS_SESSION.region_name or "ap-south-1"

    request = AWSRequest(method=method, url=url)
    signer = SigV4Auth(frozen_credentials, service, region)
    signer.add_auth(request)
    return dict(request.headers.items())
