
class Comment:

    def __init__(self,
                 author: str,
                 body: str,
                 upvotes: int,
                 downvotes: int,
                 created_utc: int,
                 edited_timestamp: int = None
                 ):
        self.author = author
        self.body = body
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.created_utc = created_utc
        self.edited_timestamp = edited_timestamp
