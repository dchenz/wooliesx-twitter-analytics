import os

import tweepy

client_key = os.environ.get("TWITTER_CLIENT_KEY")
secret_key = os.environ.get("TWITTER_SECRET_KEY")

if client_key is None or secret_key is None:
    print("failed to get .env")
    exit(1)

def get_twitter_client():
    auth = tweepy.OAuthHandler(client_key, secret_key)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def search_status_by_tags(api, tags):

    statuses = {}
    for tag in tags:
        # Get search results for tag
        tag_res = [r._json for r in api.search(q=tag, count=100)]
        # Assign search results to the tag
        statuses[tag] = tag_res

    return statuses
