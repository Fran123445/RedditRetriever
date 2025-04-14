from src.models.post import Post


class Subreddit:

    def __init__(self,
                 name: str,
                 subscribers: int,
                 posts: list[Post],
                 nsfw: bool
                 ):
        self.name = name
        self.subscribers = subscribers
        self.posts = posts
        self.nsfw = nsfw