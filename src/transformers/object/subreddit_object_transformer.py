from src.models.subreddit import Subreddit
from src.transformers.object.object_transformer import ObjectTransformer


class SubredditObjectTransformer(ObjectTransformer):

    def transform(self, raw_subreddit_json: dict):
        data = raw_subreddit_json.get("data", {})

        return Subreddit(
            subreddit_id=data.get('id', None),
            name=data.get('display_name', ''),
            subscribers=data.get('subscribers', 0),
            nsfw=data.get('over18', False),
            posts=[]
        )