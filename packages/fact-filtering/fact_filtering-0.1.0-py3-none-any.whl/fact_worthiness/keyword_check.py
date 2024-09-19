import yaml
import sys
import time
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

log_level = config['log_level']
claim_indicators = config['claim_indicators']
logger.remove()
logger.add(sys.stderr, level=log_level)

def filter_tweets_by_claim_indicators(tweets: list) -> list:
    """Filter tweets by claim indicators.

    Parameters
    ----------
    tweets : list
        The list of tweets to filter.

    Returns
    -------
    list
        The filtered list of tweets.
    """
    try:

        def check_tweet(tweet):
            matches = any(indicator.lower() in tweet.lower() for indicator in claim_indicators)
            return (tweet, 'Y' if matches else 'N')

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(check_tweet, tweets))

        return results

    except Exception as e:
        logger.error(f"An error occurred while filtering tweets by claim indicators: {e}")
        raise
