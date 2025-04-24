from src.loaders.loader import Loader


class FlairLoader(Loader):

    def load(self, data: list[tuple]):
        self._execute_sql(
            sql="""
            INSERT INTO Staging_Flair (
                internal_subreddit_id,
                text
            ) VALUES (?, ?)
            """,
            params=data
        )