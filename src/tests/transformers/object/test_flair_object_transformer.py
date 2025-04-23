import unittest

from src.models.flair import Flair
from src.transformers.object.flair_object_transformer import FlairObjectTransformer


class TestFlairObjectTransformer(unittest.TestCase):

    def test_transform_with_text_field(self):
        """
        Test that transform extracts text correctly from the _text field.
        """
        mock_raw_data = {
            "link_flair_text": "Discussion",
            "link_flair_css_class": "discussion"
        }
        transformer = FlairObjectTransformer(field_name='link_flair_text')
        flair_object = transformer.transform(mock_raw_data)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "Discussion")

    def test_transform_with_text_field_author_flair(self):
        """
        Test that transform works correctly for author_flair_text.
        """
        mock_raw_data = {
            "author_flair_text": "Moderator",
            "author_flair_css_class": "mod",
        }
        transformer = FlairObjectTransformer(field_name='author_flair_text')
        flair_object = transformer.transform(mock_raw_data)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "Moderator")


    def test_transform_with_missing_text_field(self):
        """
        Test that transform handles cases where the _text field is missing.
        """
        mock_raw_data = {
            "some_other_key": "value",
        }
        transformer = FlairObjectTransformer(field_name='link_flair_text')
        flair_object = transformer.transform(mock_raw_data)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

    def test_transform_with_null_text_field(self):
        """
        Test that transform handles cases where the _text field is explicitly null.
        Should result in an empty string for text.
        """
        mock_raw_data = {
            "link_flair_text": None,
            "link_flair_css_class": None,
        }
        transformer = FlairObjectTransformer(field_name='link_flair_text')
        flair_object = transformer.transform(mock_raw_data)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

    def test_transform_with_empty_text_field(self):
        """
        Test that transform handles cases where the _text field is an empty string.
        """
        mock_raw_data = {
            "author_flair_text": "",
            "author_flair_css_class": "user nvidia",
        }
        transformer = FlairObjectTransformer(field_name='author_flair_text')
        flair_object = transformer.transform(mock_raw_data)

        self.assertIsInstance(flair_object, Flair)
        self.assertEqual(flair_object.text, "")

if __name__ == '__main__':
    unittest.main()
