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

    def get_subreddit_posts(self, subreddit: str, limit: int = 10):
        if self.token is None:
            print("Token not available. Please call get_token() first.")
            return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "RedditRetriever/0.1 by Fran12344"
        }

        url = f"https://oauth.reddit.com/r/{subreddit}/top?limit={limit}&t=year"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None