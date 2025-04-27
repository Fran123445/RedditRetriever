from datetime import datetime

from src.models.author import Author
from src.models.comment import Comment
from src.models.flair import Flair


class Post:

    def __init__(self,
                 post_id: str,
                 title: str,
                 body: str,
                 edited_datetime: datetime,
                 upvotes: int,
                 nsfw: bool,
                 spoiler: bool,
                 author: Author,
                 flair: Flair,
                 created_datetime: datetime,
                 comments: list[Comment]
                 ):
        self.post_id = post_id
        self.title = title
        self.body = body
        self.edited_datetime = edited_datetime
        self.upvotes = upvotes
        self.nsfw = nsfw
        self.spoiler = spoiler
        self.author = author
        self.flair = flair
        self.created_datetime = created_datetime
        self.comments = comments