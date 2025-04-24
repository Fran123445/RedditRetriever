from src.loaders.loader import Loader


class CommentLoader(Loader):

    def load(self, data: list[tuple]):
        self._execute_sql(
            sql="""
            INSERT INTO Staging_Comment (
                internal_reddit_id,
                internal_post_id,
                internal_author_id,
                internal_subreddit_id,
                internal_parent_comment_id,
                body,
                edited_date,
                upvotes,
                downvotes,
                creation_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            params=data
        )