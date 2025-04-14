from src.models.subreddit import Subreddit
from src.transformers.transformer import Transformer


class SubredditTransformer(Transformer):

    def transform(self, raw_subreddit_json: dict):
        data = raw_subreddit_json.get("data", {})

        return Subreddit(
            name=data.get('display_name', ''),
            subscribers=data.get('subscribers', 0),
            nsfw=data.get('over18', False),
            posts=[]
        )