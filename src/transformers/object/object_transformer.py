from datetime import datetime


class ObjectTransformer:

    def transform(self, json: dict):
        pass

    def _timestamp_to_datetime(self, timestamp: int):
        if not timestamp:
            return None

        return datetime.fromtimestamp(timestamp)