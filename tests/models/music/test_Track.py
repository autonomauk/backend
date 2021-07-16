import pytest
from models.music import Track
from tests.variables import SPOTIFY_TRACKS_1,TRACK_DICT_1,TRACK_DICT_2

class TestTrack:
    def test_from_spotify_object(self):
        [Track.from_spotify_object(f) for f in SPOTIFY_TRACKS_1]

    def test_track(self):
        Track(**TRACK_DICT_1)
        Track(**TRACK_DICT_2)
