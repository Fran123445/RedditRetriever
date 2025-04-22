from src.models.author import Author
from src.transformers.object.flair_object_transformer import FlairObjectTransformer
from src.transformers.object.object_transformer import ObjectTransformer


class AuthorObjectObjectTransformer(ObjectTransformer):

    def __init__(self,
                 flair_transformer: FlairObjectTransformer
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