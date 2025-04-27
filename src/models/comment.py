from datetime import datetime

from src.models.author import Author


class Comment:

    def __init__(self,
                 comment_id: str,
                 author: Author,
                 body: str,
                 edited_datetime: datetime,
                 upvotes: int,
                 created_datetime: datetime,
                 children: list["Comment"]
                 ):
        self.comment_id = comment_id
        self.author = author
        self.body = body
        self.edited_datetime = edited_datetime
        self.upvotes = upvotes
        self.created_datetime = created_datetime
        self.children = children
