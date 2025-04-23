import unittest

from src.models.flair import Flair
from src.transformers.object.flair_object_transformer import FlairObjectTransformer


class TestFlairObjectTransformer(unittest.TestCase):
    LINK_FLAIR_VALID_DATA = {
        "link_flair_text": "Discussion",
        "link_flair_css_class": "discussion",
        "link_flair_text_color": "dark",  # Example of ignored field
    }

    AUTHOR_FLAIR_VALID_DATA = {
        "author_flair_text": "Moderator",
        "author_flair_css_class": "mod",
        "author_flair_background_color": "#000000",  # Example of ignored field
    }

    MISSING_FLAIR_DATA = {
        "some_other_key": "value",
    }

    NULL_FLAIR_DATA = {
        "link_flair_text": None,
        "link_flair_css_class": None,
    }

    EMPTY_FLAIR_DATA = {
        "author_flair_text": "",
        "author_flair_css_class": "user nvidia",
    }

    def setUp(self):
        self.link_flair_transformer = FlairObjectTransformer(field_name='link_flair_text')
        self.author_flair_transformer = FlairObjectTransformer(field_name='author_flair_text')

    def test_transform_with_text_field(self):
        """
        Test that transform extracts text correctly from the _text field.
        """
        flair_object = self.link_flair_transformer.transform(self.LINK_FLAIR_VALID_DATA)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "Discussion")

    def test_transform_with_text_field_author_flair(self):
        """
        Test that transform works correctly for author_flair_text.
        """
        flair_object = self.author_flair_transformer.transform(self.AUTHOR_FLAIR_VALID_DATA)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "Moderator")


    def test_transform_with_missing_text_field(self):
        """
        Test that transform handles cases where the _text field is missing.
        """
        flair_object = self.link_flair_transformer.transform(self.MISSING_FLAIR_DATA)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

    def test_transform_with_null_text_field(self):
        """
        Test that transform handles cases where the _text field is explicitly null.
        Should result in an empty string for text.
        """
        flair_object = self.link_flair_transformer.transform(self.NULL_FLAIR_DATA)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

    def test_transform_with_empty_text_field(self):
        """
        Test that transform handles cases where the _text field is an empty string.
        """
        flair_object = self.author_flair_transformer.transform(self.EMPTY_FLAIR_DATA)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

if __name__ == '__main__':
    unittest.main()
