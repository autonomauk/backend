import datetime
from enum import Enum
from typing import Optional
from pydantic.fields import Field
from models.TimedBaseModel import TimedBaseModel
from utils import stats_collection


class StatTypeEnum(str, Enum):
    SPOTICRONRUNTIME = "SPOTICRONRUNTIME"
    DEFAULT = "DEFAULT"
    USERDELETION = "USERDELETION"
    USERCREATION = "USERCREATION"
    SPOTIFYREQUEST = "SPOTIFYREQUEST"


class Stat(TimedBaseModel):
    stat: Optional[StatTypeEnum] = StatTypeEnum.DEFAULT


class CountedStatByHour(Stat):
    timestamp_hour: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.utcnow().replace(
            minute=0, second=0, microsecond=0),
        description="Hourly timestamp"
    )
    counter: Optional[int] = 0


class TimedStat(Stat):
    time: float = Field(description="Time in seconds")


class RunTime(TimedStat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.SPOTICRONRUNTIME


class UserDeletion(Stat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.USERDELETION


class UserCreation(Stat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.USERCREATION


class SpotifyRequestCalled(CountedStatByHour):
    stat: Optional[StatTypeEnum] = StatTypeEnum.SPOTIFYREQUEST


class StatsRepository:
    @staticmethod
    def spoticron_run_time(run_time: RunTime) -> RunTime:
        result = stats_collection.insert_one(run_time.dict())
        assert result.acknowledged
        return run_time

    @staticmethod
    def user_creation() -> UserCreation:
        user_creation = UserCreation()
        result = stats_collection.insert_one(user_creation.dict())
        assert result.acknowledged
        return user_creation

    @staticmethod
    def user_deletion() -> UserDeletion:
        user_deletion = UserDeletion()
        result = stats_collection.insert_one(user_deletion.dict())
        assert result.acknowledged
        return user_deletion

    def spotify_request_called() -> None:
        query = SpotifyRequestCalled().dict()
        createdAt = query.pop('createdAt')
        updatedAt = query.pop('updatedAt')
        query.pop('counter')
        result = stats_collection.update_one(query, {"$inc": {"counter": 1}, "$set": {
                                             "updatedAt": updatedAt}, "$min": {"createdAt": createdAt}}, upsert=True)
        assert result.acknowledged
