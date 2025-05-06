import dotenv
import logging
from .routes.keywords import keyword_analysis
from .routes.sentiments import sentiment_analysis
from .routes.twitter_status import twitter_status
from flask import Flask, request

dotenv.load_dotenv()

logging.basicConfig(
    filename="./server.log",
    filemode="a",
    format="%(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
)

server = Flask(__name__)


@server.route("/twitter/status", methods=["GET"])
def route_twitter_status():
    logging.info(f"GET {request.full_path} {request.remote_addr}")
    return twitter_status()


@server.route("/azure/keyword-analysis", methods=["POST"])
def route_keyword_analysis():
    logging.info(f"POST {request.full_path} {request.remote_addr}")
    return keyword_analysis()


@server.route("/azure/sentiment-analysis", methods=["POST"])
def route_sentiment_analysis():
    logging.info(f"POST {request.full_path} {request.remote_addr}")
    return sentiment_analysis()


if __name__ == "__main__":
    server.run(port=5000)
