import httpx
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class RedditAccess:

    REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
    GRANT_TYPE =  "client_credentials"
    USER_AGENT = os.getenv("USER_AGENT")

    def __init__(self,
                 httpx_session: httpx.AsyncClient,
                 ):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None
        self.session = httpx_session

    async def get_token(self):
        encoded_credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "User-Agent": RedditAccess.USER_AGENT
        }

        data = {
            "grant_type": RedditAccess.GRANT_TYPE
        }

        response = await self.session.post(
            RedditAccess.REDDIT_TOKEN_URL,
            headers=headers,
            data=data
        )

        response.raise_for_status()

        token_data = response.json()
        token = token_data["access_token"]

        self.token = token
        return token

    async def call_api(self, endpoint, params=None):
        if self.token is None:
            print("Token not available. Please call get_token() first.")
            return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": RedditAccess.USER_AGENT
        }

        url = f"https://oauth.reddit.com{endpoint}"

        response = await self.session.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        return response.json()

    async def get_subreddit_data(self, subreddit_name):
        return await self.call_api(f"/r/{subreddit_name}/about")

    async def get_post_list(self,
                      subreddit: str,
                      timeframe: str = "all",
                      limit: int = 10):
        params = {
            "limit": limit,
            "t": timeframe
        }

        return await self.call_api(f"/r/{subreddit}/top", params=params)

    async def get_comments(self,
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

        return await self.call_api(f"/r/{subreddit}/comments/{post_id}", params=params)