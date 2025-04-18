from src.models.comment import Comment
from src.transformers.author_transformer import AuthorTransformer
from src.transformers.transformer import Transformer


class CommentTransformer(Transformer):

    def __init__(self,
                 author_transformer: AuthorTransformer):
        self.author_transformer = author_transformer

    def transform(self, raw_post_comments_json: dict):
        data = raw_post_comments_json.get("data", {})
        children = data.get("children", [])

        comments = []

        for child in children:
            child_data = child.get("data", {})

            replies = self.transform(child_data["replies"]) if child_data.get("replies") else []

            comment = Comment(
                comment_id=child_data.get('id'),
                author=self.author_transformer.transform(child_data),
                body=child_data.get('body'),
                edited_timestamp=child_data.get('edited'),
                upvotes=child_data.get('ups'),
                downvotes=child_data.get('downs'),
                created_utc=child_data.get('created_utc'),
                children=replies
            )

            comments.append(comment)

        return comments
