import json

from flask import request
from flask_api import status

from .azure_api import (fetch_cached_response, generate_hash,
                        get_cognitive_services_client, save_cached_response,
                        send_statuses_to_azure)

def sentiment_analysis():
    try:
        data = request.get_json()
        client = get_cognitive_services_client()
        cache_filename = f'api_cache/{generate_hash(data["documents"], "sentiment")}.json'

        # Fetch response if it exists
        cached = fetch_cached_response(cache_filename)
        if cached is not None:
            return cached

        responses = send_statuses_to_azure(data["documents"], client.analyze_sentiment)
        sentiments = []
        for response in responses:
            sentiments.append({
                "sentiment": response.sentiment,
                "scores": {
                    "positive": response.confidence_scores.positive,
                    "neutral": response.confidence_scores.neutral,
                    "negative": response.confidence_scores.negative
                }
            })

        # Save response
        save_cached_response(cache_filename, sentiments)

        return json.dumps(sentiments)
    except ValueError:
        return ({"message": "Bad request."}, status.HTTP_400_BAD_REQUEST)
