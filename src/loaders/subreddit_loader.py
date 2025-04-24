from src.loaders.loader import Loader


class SubredditLoader(Loader):

    def load(self, data: list[tuple]):
        if not isinstance(data, list):
            # This is a workaround for the fact that the data is a list of tuples,
            # but instead I pass a single subreddit tuple
            data = [data]

        self._execute_sql(
            sql="""
            INSERT INTO Staging_Subreddit (
                internal_reddit_id,
                name,
                subscribers,
                nsfw
            ) VALUES (?, ?, ?, ?)
            """,
            params=data
        )