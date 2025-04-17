from src.models.flair import Flair


class Author:

    def __init__(self,
                 author_id: str,
                 username: str,
                 flair: Flair
                 ):
        self.author_id = author_id
        self.username = username
        self.flair = flair