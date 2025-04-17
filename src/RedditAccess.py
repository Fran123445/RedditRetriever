import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class RedditAccess:

    REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
    GRANT_TYPE =  "client_credentials"

    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None

    def get_token(self):
        encoded_credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "User-Agent": "RedditRetriever/0.1 by Fran12344"
        }

        data = {
            "grant_type": RedditAccess.GRANT_TYPE
        }

        response = requests.post(RedditAccess.REDDIT_TOKEN_URL, headers=headers, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            return True

        print(f"Error: {response.status_code} - {response.text}")
        return False

    def call_api(self, endpoint, params=None):
        if self.token is None:
            print("Token not available. Please call get_token() first.")
            return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "RedditRetriever/0.1 by Fran12344"
        }

        url = f"https://oauth.reddit.com{endpoint}"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_subreddit_data(self, subreddit_name):
        return self.call_api(f"/r/{subreddit_name}/about")

    def get_post_list(self,
                      subreddit: str,
                      timeframe: str = "all",
                      limit: int = 10):
        params = {
            "limit": limit,
            "t": timeframe
        }

        return self.call_api(f"/r/{subreddit}/top", params=params)

    def get_comments(self,
                     subreddit: str,
                     post_id: str,
                     sort: str = "best",
                     depth: int = 10,
                     limit: int = 1000):
        params = {
            "sort": sort,
            "depth": depth,
            "limit": limit
        }

        return self.call_api(f"/r/{subreddit}/comments/{post_id}", params=params)