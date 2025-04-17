from src.models.flair import Flair
from src.transformers.transformer import Transformer


class FlairTransformer(Transformer):

    def __init__(self,
                 field_name: str,
                 ):
        self.field_name = field_name

    def transform(self, data: dict):
        flair_text = data.get(self.field_name)

        if flair_text:
            return Flair(flair_text)

        return None