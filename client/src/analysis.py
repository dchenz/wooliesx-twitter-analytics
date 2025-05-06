from src import azure_api

# Assign the results to the datatset


def assign_status_keywords(statuses_by_tag):
    # Get keywords on all statuses
    for entity in statuses_by_tag.values():
        statuses_text = [s["text"] for s in entity["statuses"]]
        keywords = azure_api.get_keyword_analysis(statuses_text)
        entity["keyword"] = keywords


def assign_status_sentiments(statuses_by_tag):
    # Get sentiment on all statuses
    for entity in statuses_by_tag.values():
        statuses_text = [s["text"] for s in entity["statuses"]]
        sentiments = azure_api.get_sentiment_analysis(statuses_text)
        entity["sentiment"] = sentiments


# Group results


def get_distinct_keywords(entity):
    keyword_results = entity["keyword"]
    distinct_words = set()
    for keywords in keyword_results:
        distinct_words.update(keywords)
    return sorted(distinct_words)


def get_average_sentiment_by_keyword(entity, keyword):
    keyword_results = entity["keyword"]
    sentiment_results = entity["sentiment"]
    total_sentiment = {"positive": 0, "neutral": 0, "negative": 0}
    frequency = 0
    for status_index, keywords in enumerate(keyword_results):
        if keyword in keywords:
            status_sentiment = sentiment_results[status_index]["scores"]
            total_sentiment["positive"] += status_sentiment["positive"]
            total_sentiment["neutral"] += status_sentiment["neutral"]
            total_sentiment["negative"] += status_sentiment["negative"]
            frequency += 1
    assert frequency > 0
    return ({k: v / frequency for k, v in total_sentiment.items()}, frequency)


def group_keyword_by_sentiment(entity):
    distinct_keywords = get_distinct_keywords(entity)

    positive = []
    neutral = []
    negative = []
    mixed = []

    for keyword in distinct_keywords:
        avg_sentiment, frequency = get_average_sentiment_by_keyword(entity, keyword)

        positive_score = avg_sentiment["positive"]
        neutral_score = avg_sentiment["neutral"]
        negative_score = avg_sentiment["negative"]

        # Coutn number of occurences
        keyword_sentiment = (keyword, frequency, avg_sentiment)

        # Class the sentiments as one of the labels
        if positive_score >= neutral_score + negative_score:
            positive.append(keyword_sentiment)
        elif negative_score >= positive_score + neutral_score:
            negative.append(keyword_sentiment)
        elif neutral_score >= positive_score + negative_score:
            neutral.append(keyword_sentiment)
        else:
            mixed.append(keyword_sentiment)

    return {
        "positive": sorted(positive, key=lambda x: (-x[2]["positive"], -x[1], x[0])),
        "neutral": sorted(neutral, key=lambda x: (-x[2]["neutral"], -x[1], x[0])),
        "negative": sorted(negative, key=lambda x: (-x[2]["negative"], -x[1], x[0])),
        "mixed": sorted(mixed, key=lambda x: (-x[1], x[0])),
    }
