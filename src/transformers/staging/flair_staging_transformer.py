from src.models.comment import Comment
from src.models.subreddit import Subreddit
from src.transformers.staging.staging_transformer import StagingTransformer


class FlairStagingTransformer(StagingTransformer):

    def transform(self,
                  subreddit: Subreddit):

        flairs = set([post.flair.text if post.flair else None for post in subreddit.posts])

        for post in subreddit.posts:
            self._get_flairs_from_comments(post.comments, flairs)

        return [(subreddit.subreddit_id, flair) for flair in flairs]


    def _get_flairs_from_comments(self,
                                  comments: list[Comment],
                                  flair_set: set):
        for comment in comments:
            flair_set.add(comment.author.flair.text if comment.author.flair else None)
            self._get_flairs_from_comments(comment.children, flair_set)