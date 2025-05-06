import os
import dotenv

from src import (analysis, arguments, create_users, twitter_api, twitter_graph,
                 utils)
from src.australian import is_australian_location

if __name__ == "__main__":

    args = arguments.parse_arguments()
    dotenv.load_dotenv()

    if args.mode == "create_users":

        users = create_users.generate(args.n, include_celebrity=args.include_celebrity)
        if args.include_celebrity:
            print(users["celebrity"], "is a celebrity!")
        utils.save_json("users.json", users)

    elif args.mode == "importance":

        users = utils.read_json(args.users_path)
        ranks = twitter_graph.rank_importance(users)
        for score, screen_name in ranks:
            print(score, screen_name)

    elif args.mode == "search_tags":

        if not os.path.isdir("twitter_statuses"):
            os.mkdir("twitter_statuses")
        search_results = twitter_api.get_status_by_tags(args.tags)
        for tag, results in search_results.items():
            australian_results = list(filter(lambda s: is_australian_location(s["user"]["location"]), results))
            filename = tag.replace(" ", "_").replace("#", "")
            path = f'twitter_statuses/{filename}.json'
            utils.save_json(path, australian_results)

    elif args.mode == "keyword_sentiment":

        statuses_by_tag = utils.load_directory_json("twitter_statuses")

        # Use API to do machine learning analysis
        analysis.assign_status_keywords(statuses_by_tag)
        analysis.assign_status_sentiments(statuses_by_tag)

        if not os.path.isdir("analysis_results"):
            os.mkdir("analysis_results")

        output_csv_filename = f'analysis_results/out_{utils.get_random_hex(8)}.csv'
        output_csv = open(output_csv_filename, "w")

        csv_headers = [
            "Hashtag",
            "Keyword",
            "Sentiment",
            "Frequency",
            "Positive (%)",
            "Neutral (%)",
            "Negative (%)"
        ]
        output_csv.write(",".join(csv_headers) + "\n")
        for tag, entity in statuses_by_tag.items():
            keyword_sentiments = analysis.group_keyword_by_sentiment(entity)
            for label, result in keyword_sentiments.items():
                for keyword, freq, scores in result:
                    output_csv_line = [tag]
                    output_csv_line.append(f'"{keyword}"')
                    output_csv_line.append(label.upper())
                    output_csv_line.append(str(freq))
                    output_csv_line.append(f'{scores["positive"]:.6f}')
                    output_csv_line.append(f'{scores["neutral"]:.6f}')
                    output_csv_line.append(f'{scores["negative"]:.6f}')
                    output_csv.write(",".join(output_csv_line) + "\n")

        print("Results saved:", output_csv_filename)

