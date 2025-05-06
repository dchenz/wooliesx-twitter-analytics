import re
import requests
from src.api_config import SERVER_URL


def get_keyword_analysis(statuses):
    data = {"documents": [cleanse_twitter_status(s) for s in statuses]}
    response = requests.post(SERVER_URL + "/azure/keyword-analysis", json=data)
    analysis = response.json()
    return analysis


def get_sentiment_analysis(statuses):
    data = {"documents": [cleanse_twitter_status(s) for s in statuses]}
    response = requests.post(SERVER_URL + "/azure/sentiment-analysis", json=data)
    analysis = response.json()
    return analysis


def cleanse_twitter_status(text):
    return re.sub(r"[^\s]*https?://[^\s]+", "", text)
