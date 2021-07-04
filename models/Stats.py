
import datetime
from enum import Enum
from models.TimedBaseModel import TimedBaseModel
from typing import Optional
from pydantic.fields import Field

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

class RunTimeStat(TimedStat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.SPOTICRONRUNTIME


class UserDeletionStat(Stat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.USERDELETION


class UserCreationStat(Stat):
    stat: Optional[StatTypeEnum] = StatTypeEnum.USERCREATION


class SpotifyRequestCalledStat(CountedStatByHour):
    stat: Optional[StatTypeEnum] = StatTypeEnum.SPOTIFYREQUEST

