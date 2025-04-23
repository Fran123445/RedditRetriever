import unittest

from src.models.subreddit import Subreddit
from src.transformers.object.subreddit_object_transformer import SubredditObjectTransformer


class TestSubredditObjectTransformer(unittest.TestCase):
    VALID_JSON = {
        "kind": "t5",
        "data": {
            "user_flair_background_color": None,  # Ignored
            "id": "2qoip",
            "display_name": "laptops",
            "subscribers": 185807,
            "over18": False,
            "public_description": "The place to discuss anything laptop related.",  # Ignored
            "random_other_key": "some value"  # Ignored
        }
    }

    MISSING_DATA_KEY_JSON = {
        "kind": "t5",
        # 'data' key is missing
    }

    MISSING_INNER_KEYS_JSON = {
        "kind": "t5",
        "data": {
            "id": "km3h7f",
            "subscribers": 500,  # Present
            # display_name and over18 are missing, should default
        }
    }

    def setUp(self):
        self.transformer = SubredditObjectTransformer()

    def test_transform_valid_json(self):
        """
        Test a valid JSON.
        """
        subreddit_object = self.transformer.transform(self.VALID_JSON)

        self.assertIsInstance(subreddit_object, Subreddit)
        self.assertEqual(subreddit_object.subreddit_id, "2qoip")
        self.assertEqual(subreddit_object.name, "laptops")
        self.assertEqual(subreddit_object.subscribers, 185807)
        self.assertEqual(subreddit_object.nsfw, False)
        self.assertEqual(subreddit_object.posts, [])

    def test_transform_json_missing_data_key(self):
        """
        Test that transform handles a JSON missing the 'data' key gracefully.
        """
        subreddit_object = self.transformer.transform(self.MISSING_DATA_KEY_JSON)

        self.assertIsInstance(subreddit_object, Subreddit)
        self.assertIsNone(subreddit_object.subreddit_id)
        self.assertEqual(subreddit_object.name, "")
        self.assertEqual(subreddit_object.subscribers, 0)
        self.assertEqual(subreddit_object.nsfw, False)
        self.assertEqual(subreddit_object.posts, [])

    def test_transform_json_missing_inner_keys(self):
        """
        Test that transform handles a JSON with 'data' but missing some inner keys.
        """
        subreddit_object = self.transformer.transform(self.MISSING_INNER_KEYS_JSON)

        self.assertIsInstance(subreddit_object, Subreddit)
        self.assertEqual(subreddit_object.subreddit_id, "km3h7f")
        self.assertEqual(subreddit_object.name, "")
        self.assertEqual(subreddit_object.subscribers, 500)
        self.assertEqual(subreddit_object.nsfw, False)
        self.assertEqual(subreddit_object.posts, [])

if __name__ == '__main__':
    unittest.main()
