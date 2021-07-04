import pymongo
from utils import stats_collection

from models.Stats import RunTimeStat, UserCreationStat, UserDeletionStat, SpotifyRequestCalledStat

class StatsRepository:
    @staticmethod
    def spoticron_run_time(run_time: RunTimeStat) -> RunTimeStat:
        result = stats_collection.insert_one(run_time.dict())
        assert result.acknowledged
        return run_time

    @staticmethod
    def user_creation() -> UserCreationStat:
        user_creation = UserCreationStat()
        result = stats_collection.insert_one(user_creation.dict())
        assert result.acknowledged
        return user_creation

    @staticmethod
    def user_deletion() -> UserDeletionStat:
        user_deletion = UserDeletionStat()
        result = stats_collection.insert_one(user_deletion.dict())
        assert result.acknowledged
        return user_deletion

    def spotify_request_called() -> None:
        query = SpotifyRequestCalledStat().dict()
        createdAt = query.pop('createdAt')
        updatedAt = query.pop('updatedAt')
        query.pop('counter')
        result = stats_collection.find_one_and_update(query, {"$inc": {"counter": 1}, "$set": {
                                             "updatedAt": updatedAt}, "$min": {"createdAt": createdAt}}, upsert=True, return_document=pymongo.collection.ReturnDocument.AFTER)
        return SpotifyRequestCalledStat(**result)