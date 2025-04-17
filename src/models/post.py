from src.models.author import Author
from src.models.comment import Comment
from src.models.flair import Flair


class Post:

    def __init__(self,
                 post_id: str,
                 title: str,
                 body: str,
                 edited_timestamp: int,
                 downvotes: int,
                 upvotes: int,
                 nsfw: bool,
                 spoiler: bool,
                 author: Author,
                 flair: Flair,
                 created_utc: int,
                 comments: list[Comment]
                 ):
        self.post_id = post_id
        self.title = title
        self.body = body
        self.edited_timestamp = edited_timestamp
        self.downvotes = downvotes
        self.upvotes = upvotes
        self.nsfw = nsfw
        self.spoiler = spoiler
        self.author = author
        self.flair = flair
        self.created_utc = created_utc
        self.comments = comments