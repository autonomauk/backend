import datetime

import pytest

from workers.SpotiCron.filter import TrackFilter


def test_trackfilter_weekly(now):
    test_dates_accept = [
        now,
        now.replace(hour=0, minute=0, second=0, microsecond=0)
    ]
    test_dates_reject = [
        now+datetime.timedelta(days=7),
        now-datetime.timedelta(days=7)
    ]

    for f in test_dates_accept:
        assert TrackFilter.weekly(f)

    for f in test_dates_reject:
        assert not TrackFilter.weekly(f)

    with pytest.raises(AssertionError):
        TrackFilter.weekly("string")


def test_trackfilter_monthly(now):
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


def test_trackfilter_now(now):
    act = TrackFilter.now()

    assert abs(act-now) < datetime.timedelta(seconds=1)
    assert abs(now-act) < datetime.timedelta(seconds=1)
