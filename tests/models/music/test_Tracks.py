from models.music import Tracks, Track
import pytest

from tests.variables import TRACK_DICT_1, TRACK_DICT_2

@pytest.fixture
def tracks1():
    yield Tracks([Track(**TRACK_DICT_1)])

@pytest.fixture
def tracks2():
    yield Tracks([Track(**TRACK_DICT_1),Track(**TRACK_DICT_2)])

class TestTracks:
    def test_sequence(self, tracks1, tracks2):
        assert tracks1[0] == Track(**TRACK_DICT_1)
        assert tracks2[0] == Track(**TRACK_DICT_1)
        assert tracks2[1] == Track(**TRACK_DICT_2)
    def test_iter(self, tracks1):
        [f for f in tracks1]
        iter(tracks1)
        list(tracks1)
        assert len(tracks1) == 1