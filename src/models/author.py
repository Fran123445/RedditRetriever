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

    def __eq__(self, other):
        if isinstance(other, Author):
            return self.author_id == other.author_id
        return False

    def __hash__(self):
        return hash(self.author_id)