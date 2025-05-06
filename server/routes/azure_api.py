import hashlib
import json
import math
import os
import time
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

key = os.environ.get("AZURE_COGNITIVE_SERVICES_KEY")
endpoint = os.environ.get("AZURE_COGNITIVE_SERVICES_ENDPOINT")

if key is None or endpoint is None:
    print("failed to get .env")
    exit(1)


def get_cognitive_services_client():
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(credential=credential, endpoint=endpoint)
    return client


def send_statuses_to_azure(statuses, api_function):

    def divide_into(items, n):
        return [items[i * n : (i + 1) * n] for i in range(math.ceil(len(items) / n))]

    responses = []
    for group in divide_into(statuses, 10):
        time.sleep(0.001)
        group_response = api_function(documents=group)
        responses.extend(group_response)

    return responses


def fetch_cached_response(cache_filename):
    if os.path.isfile(cache_filename):
        with open(cache_filename, "r") as file:
            return file.read()
    return None


def save_cached_response(cache_filename, data):
    if not os.path.isdir("api_cache"):
        os.mkdir("api_cache")
    if os.path.isfile(cache_filename):
        raise Exception("Hash collision detected!")
    else:
        with open(cache_filename, "w") as file:
            file.write(json.dumps(data))


def generate_hash(statuses, salt):
    cur_hash = hashlib.sha1(salt.encode()).digest()
    for status in sorted(statuses):
        cur_hash = hashlib.sha1(cur_hash + status.encode()).digest()
    return cur_hash.hex()
