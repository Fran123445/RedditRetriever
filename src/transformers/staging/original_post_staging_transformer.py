from src.models.subreddit import Subreddit
from src.transformers.staging.staging_transformer import StagingTransformer


class OriginalPostStagingTransformer(StagingTransformer):

    def transform(self,
                  subreddit: Subreddit):

        return [
            (post.post_id,
             subreddit.subreddit_id,
             post.author.author_id,
             post.flair.text,
             post.title,
             post.body,
             post.edited_timestamp,
             post.upvotes,
             post.downvotes,
             int(post.nsfw),
             int(post.spoiler),
             post.created_utc)

            for post in subreddit.posts
        ]