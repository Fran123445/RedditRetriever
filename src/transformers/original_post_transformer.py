from src.models.post import Post
from src.transformers.transformer import Transformer


class OriginalPostTransformer(Transformer):

    def transform(self, raw_post_json: dict):
        data = raw_post_json.get("data", {})

        return Post(
            post_id=data.get("id", None),
            title=data.get("title", ""),
            body=data.get("selftext", ""),
            edited_timestamp=data.get("edited", None),
            downvotes=data.get("downs", 0),
            upvotes=data.get("ups", 0),
            nsfw=data.get("over_18", False),
            spoiler=data.get("spoiler", False),
            author=data.get("author", ""),
            created_utc=data.get("created_utc", None),
            comments=[]
        )