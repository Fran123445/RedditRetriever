from src.models.subreddit import Subreddit
from src.transformers.staging.staging_transformer import StagingTransformer


class SubredditStagingTransformer(StagingTransformer):

    def transform(self,
                  subreddit: Subreddit):

        return (subreddit.subreddit_id,
                subreddit.name,
                subreddit.subscribers,
                int(subreddit.nsfw))