import argparse
import os
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=["create_users", "importance", "search_tags", "keyword_sentiment"],
    )
    if len(sys.argv) >= 2:
        if sys.argv[1] == "create_users":
            parser.add_argument(
                "--include-celebrity",
                action="store_true",
                help="One person will be popular?",
            )
            parser.add_argument(
                "-n", type=positive_int, default=10, help="Number of users to generate"
            )
        elif sys.argv[1] == "importance":
            parser.add_argument(
                "users_path", type=file_exists, help="File path of Twitter user file"
            )
        elif sys.argv[1] == "search_tags":
            parser.add_argument(
                "--tags", nargs="+", required=True, help="tags to search for on Twitter"
            )
    args = parser.parse_args()
    return args


# Helpful type definitions


def file_exists(file):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError(f"{file} could not be found.")
    return file


def positive_int(n):
    try:
        n = int(n)
        if n <= 0:
            raise Exception
    except:
        raise argparse.ArgumentTypeError("Integer must be non-zero.")
    return n
