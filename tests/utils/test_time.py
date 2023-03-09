import datetime

import pytest

from utils.time import get_tzaware_time, get_non_tzaware_time


@pytest.mark.parametrize(
    "fn,istzaware", [(get_tzaware_time, True), (get_non_tzaware_time, False)]
)
def test_get_time_fns(fn, istzaware):
    time: datetime.datetime = fn()

    assert isinstance(time, datetime.datetime)
    has_tz_info = time.tzinfo is not None
    assert has_tz_info == istzaware

    if has_tz_info:
        has_utc_offset = time.tzinfo.utcoffset(time) is not None
        assert has_utc_offset == istzaware
