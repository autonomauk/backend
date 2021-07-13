from models.music import Track
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

    track_log: Field(
        description="Track log",
        type= List[Track],
        default=[]
    )

class User(TimedBaseModel):

    id: Optional[PydanticObjectId] = UserFields.id

    spotifyAuthDetails: SpotifyAuthDetails = UserFields.spotifyAuthDetails

    user_id: str = UserFields.user_id

    settings: Settings = UserFields.settings

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }

    def dict(self, *args,**kwargs):
        d = TimedBaseModel.dict(self, *args,**kwargs)
        d['_id'] = d['id']
        d.pop('id')
        return d

Users = List[User]