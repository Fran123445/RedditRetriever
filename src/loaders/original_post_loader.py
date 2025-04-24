from src.loaders.loader import Loader


class OriginalPostLoader(Loader):

    def load(self, data: list[tuple]):
        self._execute_sql(
            sql="""
            INSERT INTO Staging_Post (
                internal_reddit_id,
                internal_subreddit_id,
                internal_author_id,
                flair,
                title,
                body,
                edited_date,
                upvotes,
                downvotes,
                nsfw,
                spoiler,
                creation_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            params=data
        )