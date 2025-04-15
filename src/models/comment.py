
class Comment:

    def __init__(self,
                 comment_id: str,
                 author: str,
                 body: str,
                 edited_timestamp: int,
                 upvotes: int,
                 downvotes: int,
                 created_utc: int,
                 children: list["Comment"]
                 ):
        self.comment_id = comment_id
        self.author = author
        self.body = body
        self.edited_timestamp = edited_timestamp
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.created_utc = created_utc
        self.children = children
