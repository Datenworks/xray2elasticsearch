try:
    import unzip_requirements
except ImportError:
    pass

from lib.consumer import ConsumerInputParser
import requests
from os import getenv
from requests_aws4auth import AWS4Auth
import boto3
from datetime import datetime


ES_HOST = getenv("ES_HOST")
ES_INDEX = getenv("ES_INDEX")

index = f"{ES_INDEX}-{datetime.now().date().isoformat()}"
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   'us-east-1', 'es', session_token=credentials.token)

url = f"https://{ES_HOST}/{index}/_doc"


def execute(event, context):
    input_parser = ConsumerInputParser(input_data=event)
    for trace in input_parser.iterator():
        requests.post(url, auth=awsauth, json=trace)
