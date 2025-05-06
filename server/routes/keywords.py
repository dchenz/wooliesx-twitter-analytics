import json
from .azure_api import (
    fetch_cached_response,
    generate_hash,
    get_cognitive_services_client,
    save_cached_response,
    send_statuses_to_azure,
)
from flask import request
from flask_api import status


def keyword_analysis():
    try:
        data = request.get_json()
        client = get_cognitive_services_client()
        cache_filename = f'api_cache/{generate_hash(data["documents"], "keyword")}.json'

        # Fetch response if it exists
        cached = fetch_cached_response(cache_filename)
        if cached is not None:
            return cached

        responses = send_statuses_to_azure(
            data["documents"], client.extract_key_phrases
        )
        key_phrases = [[c.lower() for c in r.key_phrases] for r in responses]

        # Save response
        save_cached_response(cache_filename, key_phrases)

        return json.dumps(key_phrases)
    except ValueError:
        return ({"message": "Bad request."}, status.HTTP_400_BAD_REQUEST)
