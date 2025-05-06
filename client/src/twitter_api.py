import requests

from src.api_config import SERVER_URL

def get_status_by_tags(tags):
    params = {"tags": tags}
    response = requests.get(SERVER_URL + "/twitter/status", params=params)
    search_results = response.json()
    return search_results
