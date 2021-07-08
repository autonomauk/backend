import datetime
from functools import lru_cache

from utils.time import get_time

class TrackFilter:
    @classmethod
    def monthly(cls, date: datetime.datetime) -> bool:
        assert isinstance(date, (datetime.date,datetime.datetime))
        now = cls.now()
        return date.month == now.month and date.year == now.year

    @staticmethod
    @lru_cache(maxsize=1)
    def now() -> datetime.datetime:
        return get_time()
