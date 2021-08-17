from pydantic.main import BaseModel
from models.ListModel import ListModel
from models.music import Track,Playlist
from models.TimedBaseModel import TimedBaseModel

class TrackLog(TimedBaseModel):
    track: Track
    playlist: Playlist

TrackLogs = list[TrackLog]

class TrackLogReturnPaginated(BaseModel):
    track_log: TrackLogs
    offset: int
    length: int
    total: int