
import datetime
import pytz

def _now() -> datetime.datetime:
    return datetime.datetime.utcnow()
def get_tzaware_time() -> datetime.datetime:
    return pytz.utc.localize(_now())
def get_non_tzaware_time() -> datetime.datetime:
    return _now()
