from os import stat
import pymongo
from utils import stats_collection

import prometheus_client

from models.Stats import RunTimeStat, UserCreationStat, UserDeletionStat, SpotifyRequestCalledStat


SPOTICRON_RUN_TIME = prometheus_client.Histogram('spoticron_run_time', 'Total time taken for spoticron to run')
SPOTICRON_TRACK_ADDED = prometheus_client.Counter('spoticron_tracks_added', 'Total tracks added to playlists')
AUTONOMA_USER_CREATED = prometheus_client.Counter('autonoma_user_created', 'Total times an account has been created')
AUTONOMA_USER_DELETED = prometheus_client.Counter('autonoma_user_deleted', 'Total times an account has been deleted')
AUTONOMA_SPOTIFY_REQUESTS = prometheus_client.Counter("autonoma_spotify_request", 'Track total spotify requests')
SPOTICRON_DISABLED = prometheus_client.Counter("spoticron_disabled", "Number of times accounts have disabled spoticron")
SPOTICRON_ENABLED = prometheus_client.Counter("spoticron_enabled", "Number of times accounts have enabled spoticron")

class StatsRepository:
    @staticmethod
    def spoticron_run_time(run_time: RunTimeStat) -> RunTimeStat:
        SPOTICRON_RUN_TIME.observe(run_time.time)
        return run_time

    @staticmethod
    def user_creation() -> UserCreationStat:
        AUTONOMA_USER_CREATED.inc()
        return UserCreationStat()

    @staticmethod
    def user_deletion() -> UserDeletionStat:
        AUTONOMA_USER_DELETED.inc()
        return UserDeletionStat()

    @staticmethod
    def spotify_request_called() -> None:
        AUTONOMA_SPOTIFY_REQUESTS.inc()

    @staticmethod
    def spoticron_enabled() -> None:
        SPOTICRON_ENABLED.inc()
    
    @staticmethod
    def spoticron_disabled() -> None:
        SPOTICRON_DISABLED.inc()

    def spoticron_tracks_added(n:int = 1) -> None:            
        SPOTICRON_TRACK_ADDED.inc(n)