from src.models.comment import Comment
from src.models.subreddit import Subreddit
from src.transformers.staging.staging_transformer import StagingTransformer


class AuthorStagingTransformer(StagingTransformer):

    def transform(self,
                  subreddit: Subreddit):

        authors_set = set([post.author for post in subreddit.posts])

        for post in subreddit.posts:
            self._get_authors_from_comments(post.comments, authors_set)

        return [(author.author_id, subreddit.subreddit_id, author.flair.text) for author in authors_set]


    def _get_authors_from_comments(self,
                                   comments: list[Comment],
                                   author_set: set):
        for comment in comments:
            author_set.add(comment.author)
            self._get_authors_from_comments(comment.children, author_set)

