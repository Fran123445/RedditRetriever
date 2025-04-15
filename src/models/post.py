from src.models.comment import Comment


class Post:

    def __init__(self,
                 title: str,
                 body: str,
                 edited_timestamp: int,
                 downvotes: int,
                 upvotes: int,
                 nsfw: bool,
                 spoiler: bool,
                 author: str,
                 created_utc: int,
                 comments: list[Comment]
                 ):
        self.title = title
        self.body = body
        self.edited_timestamp = edited_timestamp
        self.downvotes = downvotes
        self.upvotes = upvotes
        self.nsfw = nsfw
        self.spoiler = spoiler
        self.author = author
        self.created_utc = created_utc
        self.comments = comments