from src.models.comment import Comment
from src.transformers.transformer import Transformer


class CommentTransformer(Transformer):

    def transform(self, raw_post_comments_json: dict):
        data = raw_post_comments_json.get("data", {})
        children = data.get("children", [])

        comments = []

        for child in children:
            child_data = child.get("data", {})

            replies = self.transform(child_data["replies"])

            comment = Comment(
                comment_id=child_data['id'],
                author=data['author'],
                body=data['body'],
                edited_timestamp=data['edited'] if data['edited'] else None,
                upvotes=data['ups'],
                downvotes=data['downs'],
                created_utc=data['created_utc'],
                children=replies
            )

            comments.append(comment)

        return comments
