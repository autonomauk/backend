import time

from tests.variables import TRACK_DICT_1
from models.ObjectId import PydanticObjectId

from loguru import logger

from models.music import Playlist, Playlists
from workers.SpotiCron.main import SpotiCronRunnerPerUser

from models.music import Track, Tracks

def test_find_and_create_playlist(spoticron_runner: SpotiCronRunnerPerUser):
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

def test_create_playlist(spoticron_runner: SpotiCronRunnerPerUser):
    playlist: Playlist = spoticron_runner.create_playlist_for_user()
    assert len(spoticron_runner.spotify.playlist_tracks(
        playlist_id=playlist.id)['items']) == 0

def test_find_songs_in_target_playlist(spoticron_runner: SpotiCronRunnerPerUser):
    playlist: Playlist = spoticron_runner.create_playlist_for_user()
    spoticron_runner.target_playlist = playlist

    track_to_add: Track = Track(**TRACK_DICT_1)
    spoticron_runner.spotify.playlist_add_items(
        playlist_id=playlist.id, items=[track_to_add.uri])

    tracks: Tracks = spoticron_runner.find_songs_in_target_playlist()
    assert len(tracks) == 1
    assert tracks[0].uri == track_to_add.uri

def test_clean_up(spoticron_runner: SpotiCronRunnerPerUser):
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

def test_time(spoticron_runner: SpotiCronRunnerPerUser):

    total_dt = 0
    n = 10
    for _ in range(n):
        t1 = time.time()
        spoticron_runner.run()
        t2 = time.time()
        dt = t2-t1
        total_dt += dt

    assert (dt/n) < 1.0 #  Average run-time <1.0s
