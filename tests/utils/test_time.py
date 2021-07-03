import datetime
from utils import get_time

def test_get_time():
    time: datetime.datetime = get_time()

    assert isinstance(time, datetime.datetime)