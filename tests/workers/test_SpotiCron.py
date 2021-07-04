import datetime
import pytest
from workers.SpotiCron import Track, TrackFilter, Tracks


class TestTrackFilter:
    def test_monthly(self):
        now = datetime.datetime.utcnow()

        test_dates_accept = [
            now,
            now.replace(hour=0,minute=0,second=0,microsecond=0)
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
            tracks1 + tracks1