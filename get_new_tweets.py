import requests
import os
import json

# Load environment variables from .env file (if using dotenv)
from dotenv import load_dotenv
load_dotenv()

# Get the Bearer Token from the environment variable
bearer_token = os.getenv("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Parameters for the API request
query_params = {
    'query': '(from:twitterdev -is:retweet) OR #twitterdev',
    'tweet.fields': 'author_id'
}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython",
        "Content-Type": "application/json"  # Specify content type as JSON for POST request
    }
    response = requests.post(url, headers=headers, json=params)
    if response.status_code != 200:
        raise Exception(f"Error connecting to endpoint: {response.status_code} - {response.text}")
    return response.json()

def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
