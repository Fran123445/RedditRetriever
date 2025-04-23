from src.models.post import Post
from src.transformers.object.author_object_transformer import AuthorObjectObjectTransformer
from src.transformers.object.flair_object_transformer import FlairObjectTransformer
from src.transformers.object.object_transformer import ObjectTransformer


class OriginalPostObjectTransformer(ObjectTransformer):

    def __init__(self,
                 author_transformer: AuthorObjectObjectTransformer,
                 flair_transformer: FlairObjectTransformer
                 ):
        self.author_transformer = author_transformer
        self.flair_transformer = flair_transformer

    def transform(self, raw_post_json: dict):
        data = raw_post_json.get("data", {})

        edited_datetime = self._timestamp_to_datetime(data.get("edited"))
        created_datetime = self._timestamp_to_datetime(data.get("created_utc"))

        return Post(
            post_id=data.get("id"),
            title=data.get("title", ""),
            body=data.get("selftext", ""),
            edited_datetime=edited_datetime,
            downvotes=data.get("downs", 0),
            upvotes=data.get("ups", 0),
            nsfw=data.get("over_18", False),
            spoiler=data.get("spoiler", False),
            author=self.author_transformer.transform(data),
            flair=self.flair_transformer.transform(data),
            created_datetime=created_datetime,
            comments=[]
        )