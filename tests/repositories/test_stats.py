from datetime import timedelta
import pytest
import random

from repositories.stats import StatsRepository
from models.Stats import RunTimeStat, SpotifyRequestCalledStat, UserCreationStat, UserDeletionStat
from utils import stats_collection


@pytest.fixture
def run_time():
    run_time: RunTimeStat = RunTimeStat(time=round(random.random()*10, 6))

    yield run_time

    stats_collection.delete_one({'time': run_time.time, 'stat': str(
        run_time.stat), 'createdAt': run_time.createdAt})


class TestStatsRepository:
    def test_spoticron_run_time(self, run_time: RunTimeStat):
        assert run_time is not None

        StatsRepository.spoticron_run_time(run_time=run_time)

        got_run_time = RunTimeStat(
            **stats_collection.find_one({"time": run_time.time}))

        assert got_run_time.time == run_time.time
        assert got_run_time.stat == run_time.stat

    def test_user_creation(self):
        user_creation: UserCreationStat = StatsRepository.user_creation()

        got_user_creation = UserCreationStat(**stats_collection.find_one({
            "stat": user_creation.stat,
            "createdAt": {
                "$gt": user_creation.createdAt.replace(microsecond=0),
                "$lte": user_creation.createdAt+timedelta(seconds=1)
            }
        }))

        assert got_user_creation.stat == user_creation.stat
        assert got_user_creation.createdAt.replace(
            microsecond=0) == user_creation.createdAt.replace(microsecond=0)

        # tear down
        assert stats_collection.delete_one(
            {"stat": user_creation.stat, "createdAt": user_creation.createdAt}) is not None

    def test_user_deletion(self):
        user_deletion: UserDeletionStat = StatsRepository.user_deletion()

        got_user_deletion = UserDeletionStat(**stats_collection.find_one({
            "stat": user_deletion.stat,
            "createdAt": {
                "$gt": user_deletion.createdAt.replace(microsecond=0),
                "$lte": user_deletion.createdAt+timedelta(seconds=1)
            }
        }))

        assert got_user_deletion.stat == user_deletion.stat
        assert got_user_deletion.createdAt.replace(
            microsecond=0) == user_deletion.createdAt.replace(microsecond=0)

        # tear down
        assert stats_collection.delete_one(
            {"stat": got_user_deletion.stat, "createdAt": got_user_deletion.createdAt}) is not None

    def test_spotify_request_called(self):
        spotify_request_called: SpotifyRequestCalledStat = StatsRepository.spotify_request_called()

        got_spotify_request_called = SpotifyRequestCalledStat(**stats_collection.find_one({
            "stat": spotify_request_called.stat,
            "createdAt": {
                "$gt": spotify_request_called.createdAt.replace(microsecond=0),
                "$lte": spotify_request_called.createdAt+timedelta(seconds=1)
            }
        }))

        assert got_spotify_request_called.stat == spotify_request_called.stat
        assert got_spotify_request_called.createdAt.replace(
            microsecond=0) == spotify_request_called.createdAt.replace(microsecond=0)

        # tear down
        assert stats_collection.delete_one(
            {"stat": got_spotify_request_called.stat, "createdAt": got_spotify_request_called.createdAt}) is not None
