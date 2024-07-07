import requests
# # import os
import time
from datetime import datetime, timezone, timedelta
# # from dotenv import load_dotenv

# # load_dotenv()
# # bearer_token = os.getenv("BEARER_TOKEN")

# Define constants
BEARER_TOKEN = ""
SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
USER_AGENT = "v2RecentSearchPython"
CHECK_INTERVAL = 15  # Interval in seconds to check for new tweets

def get_bearer_headers(token):
    """
    Returns headers required for Bearer token authentication.
    """
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT
    }

def get_query_params(user_id, start_time):
    """
    Returns query parameters for the Twitter API request.
    """
    return {
        "query": f"from:{user_id}",
        "tweet.fields": "created_at",
        "start_time": start_time,
    }

def fetch_new_tweets(url, headers, params):
    """
    Fetches new tweets from the Twitter API endpoint.
    """
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Error connecting to endpoint: {response.status_code} - {response.text}")
    return response.json()

def print_tweet_details(tweets):
    """
    Prints the created_at and text of each tweet in the response.
    """
    for tweet in tweets:
        print(f"Tweet Created At: {tweet['created_at']}")
        print(f"Tweet Text: {tweet['text']}")
        print("-" * 40)

def get_current_utc_timestamp():
    """
    Returns the current UTC timestamp minus one minute in the required format.
    """
    return (datetime.now(timezone.utc) - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def main():
    user_id = input("Enter the user id: ")
    old_start_time = get_current_utc_timestamp()

    try:
        while True:
            headers = get_bearer_headers(BEARER_TOKEN)
            params = get_query_params(user_id, old_start_time)

            json_response = fetch_new_tweets(SEARCH_URL, headers, params)

            if "meta" in json_response and json_response["meta"]["result_count"] > 0:
                new_start_time = json_response["data"][0]["created_at"]

                if new_start_time != old_start_time:
                    print_tweet_details(json_response["data"])
                    old_start_time = new_start_time

            time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
