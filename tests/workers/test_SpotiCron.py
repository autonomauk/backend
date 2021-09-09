import datetime
import time
from tests.variables import TRACK_DICT_1
from models.ObjectId import PydanticObjectId

from loguru import logger

from repositories.user import UserRepository

import spotipy
from utils.time import get_time
from models.User import User
from models.music import Playlist, Playlists
from workers.SpotiCron.main import SpotiCronRunnerPerUser
import pytest

from models.music import Track, Tracks

from workers.SpotiCron.filter import TrackFilter

class TestTrackFilter:
    def test_monthly(self):
        now = datetime.datetime.utcnow()

        test_dates_accept = [
            now,
            now.replace(hour=0, minute=0, second=0, microsecond=0)
        ]
        test_dates_reject = [
            now+datetime.timedelta(days=60),
            now-datetime.timedelta(days=60)
        ]

        for f in test_dates_accept:
            assert TrackFilter.monthly(f)

        for f in test_dates_reject:
            assert not TrackFilter.monthly(f)

        with pytest.raises(AssertionError):
            TrackFilter.monthly("string")

    def test_now(self):
        now_dt = datetime.datetime.utcnow()
        now = TrackFilter.now()

        assert abs(now-now_dt) < datetime.timedelta(seconds=1)
        assert abs(now_dt-now) < datetime.timedelta(seconds=1)



# pylint: disable=redefined-outer-name
@pytest.fixture
def spoticron_runner():
    playlist_name: str = str(PydanticObjectId())
    user: User = UserRepository.get(PydanticObjectId('613a2cc41933ae5e743cd98f'))

    yield SpotiCronRunnerPerUser(user=user, playlist_name=playlist_name)


class TestSpotiCronRunnerPerUser:
    def test_find_and_create_playlist(self, spoticron_runner: SpotiCronRunnerPerUser):
        spoticron_runner.target_playlist = Playlist(name="TEST")
        playlist: Playlist = spoticron_runner.find_playlist()
        assert playlist is not None

        # Change target playlist
        spoticron_runner.target_playlist = Playlist(
            name=str(PydanticObjectId()))

        # Find it, but it 100% doesn't exist so we create it
        playlist: Playlist = spoticron_runner.find_playlist()
        assert playlist is None
        playlist: Playlist = spoticron_runner.create_playlist_for_user()
        assert playlist is not None

        tracks: list = spoticron_runner.spotify.user_playlist_tracks(
            playlist_id=playlist.id,
            user=spoticron_runner.user.user_id
        )['items']
        assert len(tracks) == 0

    def test_create_playlist(self, spoticron_runner: SpotiCronRunnerPerUser):
        playlist: Playlist = spoticron_runner.create_playlist_for_user()
        assert len(spoticron_runner.spotify.playlist_tracks(
            playlist_id=playlist.id)['items']) == 0

    def test_find_songs_in_target_playlist(self, spoticron_runner: SpotiCronRunnerPerUser):
        playlist: Playlist = spoticron_runner.create_playlist_for_user()
        spoticron_runner.target_playlist = playlist

        track_to_add: Track = Track(**TRACK_DICT_1)
        spoticron_runner.spotify.playlist_add_items(
            playlist_id=playlist.id, items=[track_to_add.uri])

        tracks: Tracks = spoticron_runner.find_songs_in_target_playlist()
        assert len(tracks) == 1
        assert tracks[0].uri == track_to_add.uri

    def test_clean_up(self, spoticron_runner: SpotiCronRunnerPerUser):
        playlists: Playlists = [
            Playlist(**f) for f in
            spoticron_runner.spotify.current_user_playlists(
                limit=50,
                offset=0)['items']
        ]

        for playlist in playlists:
            if playlist.name != "TEST":
                logger.debug(f"Unfollowing {playlist.name=}")
                spoticron_runner.spotify.current_user_unfollow_playlist(
                    playlist.id)

    def test_time(self, spoticron_runner: SpotiCronRunnerPerUser):
        total_dt = 0
        n = 10
        for _ in range(n):
            t1 = time.time()
            spoticron_runner.run()
            t2 = time.time()
            dt = t2-t1
            total_dt += dt

        assert (dt/n) < 1.0 #  Average run-time <1.0s
