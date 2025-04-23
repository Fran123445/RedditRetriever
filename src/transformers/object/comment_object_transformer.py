from src.models.comment import Comment
from src.transformers.object.author_object_transformer import AuthorObjectObjectTransformer
from src.transformers.object.object_transformer import ObjectTransformer


class CommentObjectTransformer(ObjectTransformer):

    def __init__(self,
                 author_transformer: AuthorObjectObjectTransformer):
        self.author_transformer = author_transformer

    def transform(self, raw_post_comments_json: dict):
        data = raw_post_comments_json.get("data", {})
        children = data.get("children", [])

        comments = []

        for child in children:
            child_data = child.get("data", {})

            replies = self.transform(child_data["replies"]) if child_data.get("replies") else []

            edited_datetime = self._timestamp_to_datetime(data.get("edited"))
            created_datetime = self._timestamp_to_datetime(data.get("created_utc"))

            comment = Comment(
                comment_id=child_data.get('id'),
                author=self.author_transformer.transform(child_data),
                body=child_data.get('body'),
                edited_datetime=edited_datetime,
                upvotes=child_data.get('ups'),
                downvotes=child_data.get('downs'),
                created_datetime=created_datetime,
                children=replies
            )

            comments.append(comment)

        return comments
