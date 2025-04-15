from src.models.post import Post


class Subreddit:

    def __init__(self,
                 subreddit_id: str,
                 name: str,
                 subscribers: int,
                 posts: list[Post],
                 nsfw: bool
                 ):
        self.subreddit_id = subreddit_id
        self.name = name
        self.subscribers = subscribers
        self.posts = posts
        self.nsfw = nsfw