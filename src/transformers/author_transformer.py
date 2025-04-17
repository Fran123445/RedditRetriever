from src.models.author import Author
from src.transformers.flair_transformer import FlairTransformer
from src.transformers.transformer import Transformer


class AuthorTransformer(Transformer):

    def __init__(self,
                 flair_transformer: FlairTransformer
                 ):
        self.flair_transformer = flair_transformer

    def transform(self, data: dict):
        author_id = data.get("author_fullname")
        username = data.get("author")
        flair = self.flair_transformer.transform(data)

        return Author(
            author_id=author_id,
            username=username,
            flair=flair
        )