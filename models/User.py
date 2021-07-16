from models.music.TrackLog import TrackLog, TrackLogs
from models.music import Track, Tracks
from models.TimedBaseModel import TimedBaseModel
from models.ObjectId import PydanticObjectId
from models.Settings import Settings
from typing import List, Optional
from models.SpotifyAuthDetails import SpotifyAuthDetails
from pydantic.fields import Field

_string = dict(min_length=1)

class UserFields:
    id = Field(
        None,
        alias="_id",
        description="UUID for user",
        type=Optional[PydanticObjectId]
    )

    user_id = Field(
        None,
        description="user_id as designated by Spotify",
        **_string
    )

    spotifyAuthDetails = Field(
        description="Spotify auth tokens"
    )

    settings = Field(
        description="User settings",
        type=Settings,
        default=Settings()
    )

    track_log = Field(
        description="Track log",
        type= TrackLogs,
        default=TrackLogs()
    )

class User(TimedBaseModel):

    id: Optional[PydanticObjectId] = UserFields.id

    spotifyAuthDetails: SpotifyAuthDetails = UserFields.spotifyAuthDetails

    user_id: str = UserFields.user_id

    settings: Settings = UserFields.settings

    track_log: TrackLogs = UserFields.track_log

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }

    def dict(self, *args, **kwargs):
        d = super(User, self).dict(*args, **kwargs)
        d['_id'] = d['id']
        d.pop('id')
        return d

Users = List[User]