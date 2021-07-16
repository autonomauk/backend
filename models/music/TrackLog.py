from models.music import Track,Playlist
from models.TimedBaseModel import TimedBaseModel

class TrackLog(TimedBaseModel):
    track: Track
    playlist: Playlist

TrackLogs = list[TrackLog]