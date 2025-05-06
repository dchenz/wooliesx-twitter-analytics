import json

from flask import request
from flask_api import status
from .twitter_api import get_twitter_client, search_status_by_tags

def twitter_status():
    tags = request.args.getlist("tags", type=str)
    if len(tags) == 0:
        return ({"message": "Bad request."}, status.HTTP_400_BAD_REQUEST)
    # Authenticate to Twitter API
    api = get_twitter_client()
    statuses = search_status_by_tags(api, tags)
    return json.dumps(statuses)

