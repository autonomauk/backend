import datetime
from models.ObjectId import PydanticObjectId

from loguru import logger

from repositories.user import UserRepository

import spotipy
from utils.time import get_time
from tests.variables import STATIC_USER_DICT
from models.User import User
from workers.SpotiCron.main import SpotiCronRunnerPerUser
import pytest

from workers.SpotiCron.models import Playlist, Playlists, Track, Tracks
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


class TestModels:
    def test_tracks(self):
        shared_track = Track(id="foo")
        new_track = Track(id="bar")
        tracks1 = Tracks(tracks=[shared_track])
        tracks2 = Tracks(tracks=[new_track, shared_track])

        diff_tracks = tracks1 - tracks1
        assert len(diff_tracks) == 0

        diff_tracks = tracks2 - tracks1
        assert len(diff_tracks) == 1
        assert diff_tracks[0] == new_track

        diff_tracks = tracks1 - tracks2
        assert len(diff_tracks) == 0

        with pytest.raises(TypeError):
            tracks1 + tracks1  # pylint: disable=pointless-statement

        assert tracks1[0] == shared_track
        assert tracks2[1] == shared_track

# pylint: disable=redefined-outer-name


@pytest.fixture
def spoticron_runner():
    playlist_name: str = str(PydanticObjectId())
    user: User = User(**STATIC_USER_DICT)

    UserRepository.create(user)

    yield SpotiCronRunnerPerUser(user=user, playlist_name=playlist_name)
    UserRepository.delete(user.id)


class TestSpotiCronRunnerPerUser:
    def test_init(self, spoticron_runner: SpotiCronRunnerPerUser):
        assert isinstance(spoticron_runner, SpotiCronRunnerPerUser)
        assert isinstance(spoticron_runner.spotify, spotipy.Spotify)
        assert isinstance(spoticron_runner.target_playlist, Playlist)
        assert isinstance(spoticron_runner.user, User)

        assert spoticron_runner.user.spotifyAuthDetails.expires_at.replace(
            tzinfo=None) >= get_time()
        assert spoticron_runner.user.spotifyAuthDetails.access_token is not STATIC_USER_DICT[
            'spotifyAuthDetails']['access_token']
        assert spoticron_runner.user.spotifyAuthDetails.refresh_token is STATIC_USER_DICT[
            'spotifyAuthDetails']['refresh_token']

        updated_user: User = UserRepository.get(spoticron_runner.user.id)
        spoticron_runner_user = spoticron_runner.user

        assert updated_user.spotifyAuthDetails.access_token == spoticron_runner_user.spotifyAuthDetails.access_token
        assert updated_user.spotifyAuthDetails.refresh_token == spoticron_runner_user.spotifyAuthDetails.refresh_token
        assert updated_user.user_id == spoticron_runner_user.user_id

    def test_find_and_create_playlist(self, spoticron_runner: SpotiCronRunnerPerUser):
        spoticron_runner.target_playlist = Playlist(name="TEST")
        playlist: Playlist = spoticron_runner.find_playlist()
        assert playlist is not None

        # Change target playlist
        spoticron_runner.target_playlist = Playlist(
            name=str(PydanticObjectId()))

        # Find it, but it 100% doesn't exist so we create it
        playlist: Playlist = spoticron_runner.find_playlist()
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

        track_to_add: Track = Track(id="6GPpocnUJbzMNMTJDLYCim")
        spoticron_runner.spotify.playlist_add_items(
            playlist_id=playlist.id, items=[track_to_add.id])

        tracks: Tracks = spoticron_runner.find_songs_in_target_playlist()
        assert len(tracks) == 1
        assert tracks[0].id == track_to_add.id

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
