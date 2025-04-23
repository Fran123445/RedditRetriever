
class Flair():

    def __init__(self,
                 text: str
                 ):
        self.text = text

    def __eq__(self, other):
        if isinstance(other, Flair):
            return self.text == other.text
        return False

    def __hash__(self):
        return hash(self.text)