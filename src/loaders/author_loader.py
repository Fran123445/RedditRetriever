from src.loaders.loader import Loader


class AuthorLoader(Loader):

    def load(self, data: list[tuple]):
        self._execute_sql(
            sql="""
            INSERT INTO Staging_Author (
                internal_reddit_id,
                internal_subreddit_id,
                username,
                flair
            ) VALUES (?, ?, ?, ?)
            """,
            params=data
        )