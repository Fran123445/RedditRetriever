from src.models.comment import Comment
from src.models.post import Post
from src.models.subreddit import Subreddit
from src.transformers.staging.staging_transformer import StagingTransformer


class CommentStagingTransformer(StagingTransformer):

    def transform(self,
                  subreddit: Subreddit):

        staging_comments_list = []

        for post in subreddit.posts:
            self._transform_comments(subreddit, post, None, post.comments, staging_comments_list)

        return staging_comments_list

    def _transform_comments(self,
                            subreddit: Subreddit,
                            post: Post,
                            parent_comment: Comment,
                            comments: list[Comment],
                            staging_comments_list: list):

        for comment in comments:
            staging_comments_list.append(
                (comment.comment_id,
                 post.post_id,
                 comment.author.author_id,
                 subreddit.subreddit_id,
                 parent_comment.comment_id if parent_comment else None,
                 comment.body,
                 comment.edited_datetime,
                 comment.upvotes,
                 comment.downvotes,
                 comment.created_datetime)
            )

            if comment.children:
                self._transform_comments(subreddit, post, comment, comment.children, staging_comments_list)