# WooliesX Twitter Analytics

The Twitter API imposes rate limits on the number of API calls in a 15 minute window. A large volume of Twitter statuses, hashtags and user profiles are required to effectively analyse data. The code in this repository is designed to use the Twitter API to collect data, however locally-generated data will be used where possible to shorten the demonstration.

## 1. PageRank

PageRank is an algorithm used by Google to measure the importance of a set of websites. Websites may contain hyperlinks to other websites (outgoing edges) and be hyperlinked by other websites (incoming edges). A website's importance depends on the total importance of incoming edges and the number of outgoing edges. The output of the PageRank algorithm is a ranking of entities in decreasing order of importance.

Twitter users can be represented using a graph data structure. Usernames (or IDs) form the vertices, while an outgoing edge exists from A to B if and only if A is following B on Twitter. Users receive higher importance if they are followed by other Twitter users with high importance. Importance is decreased if the user follows a large number of other Twitter users.

By this logic, we can use PageRank to help our data analysis:

- Spam bot accounts typically have very few followers, or lots of spam bot followers with low importance, and they follow a lot of users. The algorithm will assign them low importance.
- Celebrities (or influencers) have lots of followers from normal users and they don't follow many people. The algorithm will assign them a high importance.
- Normal users' importances are somewhere in between depending on their follower-following relationships.

For demonstration, the following commands run PageRank against a set of Twitter users with and without a celebrity. The celebrity is programmed such that any Twitter user, not already following them, has a 50% chance of following them.

```sh
# Generate 100 Twitter users and save to 'users.json'.

$ python3 run.py create_users -n 100

# Generate 100 Twitter users and save to 'users.json'.
# However, one user is more likely to be popular.

$ python3 run.py create_users -n 100 --include-celebrity
noah_martinez957 is a celebrity!
```

To generate and view importance of the users that we have created:

```sh
# Load the output file from the code above
# Note that our celebrity has the highest score

$ python3 run.py importance users.json
0.0024090020 noah_martinez957
0.0019140071 raymond_lewis221
0.0018112471 frances_anderson962
0.0016796391 raymond_roberts549
0.0016492986 michael_lewis190
0.0016326202 christian_white530
0.0016272006 jordan_baker49
0.0016067974 aaron_sanchez338
...
```

## 2. Search Twitter statuses by #hashtag

```sh
# Get hashtags #woolies, #coles and #aldi.
# Can also combine multiple hashtags into one query.

$ python3 run.py search_tags --tags "#woolies OR #woolworths" "#coles" "#aldi" "#groceries"
Saving to file: twitter_statuses/woolies_OR_woolworths.json
Saving to file: twitter_statuses/coles.json
Saving to file: twitter_statuses/aldi.json
Saving to file: twitter_statuses/groceries.json

# View the saved results

ls twitter_statuses
aldi.json  coles.json groceries.json woolies_OR_woolworths.json
```

## 3. Sentiment and keyword analysis on Twitter statuses

Sentiment analysis is a machine learning technique used to label text as "positive", "neutral" or "negative". Keyword (or key phrases) analysis is similar technique used to retrieve the main topic of a text sample. Natural language processing enables users to parse and assign programmatic meaning to unstructured bodies of text from any human language (not just English!).

This function requires Twitter statuses to be already downloaded to the `twitter_statuses` folder (Step 2).

Results are saved to a CSV file inside the directory `analysis_results`. It can be loaded into BI tools such as Power BI or Tableau for analysis and visualisation.

```sh
# Perform sentiment and keyword analysis on Twitter statuses.
# Save results to CSV file.

$ python3 run.py keyword_sentiment
Reading from file: twitter_statuses/aldi.json
Reading from file: twitter_statuses/coles.json
Reading from file: twitter_statuses/groceries.json
Reading from file: twitter_statuses/woolies_OR_woolworths.json
Results saved: analysis_results/out_4410cc1F.csv # Random file name

# It groups keywords of Twitter statuses by sentiment and by hashtag (e.g. #woolies)
# The output below has been shortened for demonstration purposes.

$ cat analysis_results/out_4410cc1F.csv
Hashtag,Keyword,Sentiment,Frequency,Positive (%),Neutral (%),Negative (%)
...
groceries,"nice cold glass",POSITIVE,2,1.000000,0.000000,0.000000
groceries,"africandelicacies",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"evom",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"foodie",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"good #food",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"good #time",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"grocery shopping",POSITIVE,1,1.000000,0.000000,0.000000
groceries,"best shopping exp",POSITIVE,1,0.990000,0.010000,0.000000
...
woolies_OR_woolworths,"baby",POSITIVE,2,1.000000,0.000000,0.000000
woolies_OR_woolworths,"other great creat",POSITIVE,2,1.000000,0.000000,0.000000
woolies_OR_woolworths,"butter scones",POSITIVE,1,1.000000,0.000000,0.000000
woolies_OR_woolworths,"cream gratin",POSITIVE,1,1.000000,0.000000,0.000000
woolies_OR_woolworths,"lilolam7",POSITIVE,1,1.000000,0.000000,0.000000
woolies_OR_woolworths,"potato",POSITIVE,1,1.000000,0.000000,0.000000
woolies_OR_woolworths,"yummy",POSITIVE,1,1.000000,0.000000,0.000000
woolies_OR_woolworths,"home",POSITIVE,3,0.996667,0.003333,0.000000
...
woolies_OR_woolworths,"isolation",NEGATIVE,2,0.000000,0.000000,1.000000
woolies_OR_woolworths,"toilet paper thing",NEGATIVE,2,0.000000,0.000000,1.000000
woolies_OR_woolworths,"toiletpaper",NEGATIVE,2,0.000000,0.000000,1.000000
woolies_OR_woolworths,"2 week lockdown",NEGATIVE,1,0.000000,0.000000,1.000000
woolies_OR_woolworths,"cupboard",NEGATIVE,1,0.000000,0.000000,1.000000
woolies_OR_woolworths,"day",NEGATIVE,1,0.000000,0.000000,1.000000
woolies_OR_woolworths,"early durin",NEGATIVE,1,0.000000,0.000000,1.000000
woolies_OR_woolworths,"essential food shopping",NEGATIVE,1,0.000000,0.000000,1.000000
...
```
