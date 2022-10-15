import prometheus_client

from config import settings


from models.Stats import RunTimeStat, UserCreationStat, UserDeletionStat

SPOTICRON_RUN_TIME = prometheus_client.Histogram('spoticron_run_time', 'Total time taken for spoticron to run', buckets=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,2.0,5.0,10.0,float('inf')))
SPOTICRON_RUNS = prometheus_client.Counter('spoticron_runs', 'Total spoticron runs')
SPOTICRON_TRACK_ADDED = prometheus_client.Counter('spoticron_tracks_added', 'Total tracks added to playlists',['id'])
AUTONOMA_USER_CREATED = prometheus_client.Counter('autonoma_api_user_created', 'Total times an account has been created')
AUTONOMA_USER_DELETED = prometheus_client.Counter('autonoma_api_user_deleted', 'Total times an account has been deleted')
SPOTICRON_SPOTIFY_REQUESTS = prometheus_client.Counter("spoticron_spotify_request", 'Track total spotify requests')
SPOTICRON_DISABLED = prometheus_client.Counter("spoticron_disabled", "Number of times accounts have disabled spoticron")
SPOTICRON_ENABLED = prometheus_client.Counter("spoticron_enabled", "Number of times accounts have enabled spoticron")

AUTONOMA_BUILD = prometheus_client.Info('autonoma_api_build', "Information about the backend build")
AUTONOMA_BUILD.info({'version':settings.VERSION})

class StatsRepository:
    @staticmethod
    def spoticron_run_time(run_time: RunTimeStat) -> RunTimeStat:   
        SPOTICRON_RUN_TIME.observe(run_time.time)
        return run_time

    @staticmethod
    def spoticron_run() -> None:
        SPOTICRON_RUNS.inc()

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
        SPOTICRON_SPOTIFY_REQUESTS.inc()

    @staticmethod
    def spoticron_enabled() -> None:
        SPOTICRON_ENABLED.inc()
    
    @staticmethod
    def spoticron_disabled() -> None:
        SPOTICRON_DISABLED.inc()

    @staticmethod
    def spoticron_tracks_added(n:int = 1, id = None) -> None:
        SPOTICRON_TRACK_ADDED.labels(id=id).inc(n)