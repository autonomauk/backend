from bson.objectid import ObjectId
from models.ObjectId import PydanticObjectId
from utils.time import get_time
from models.Settings import Settings
from typing import List, Optional, Set
from models.SpotifyAuthDetails import SpotifyAuthDetailsFields, SpotifyAuthDetails
import datetime
from pydantic import BaseModel
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

    createdAt = Field(
        description="Created at datetime",
        type=datetime.datetime,
        default_factory=lambda: get_time()
    )

    updatedAt = Field(
        description="Created at datetime",
        type=datetime.datetime,
        default_factory=lambda: get_time()
    )


class User(BaseModel):

    createdAt: Optional[datetime.datetime] = UserFields.createdAt

    updatedAt: Optional[datetime.datetime] = UserFields.updatedAt

    id: Optional[PydanticObjectId] = UserFields.id

    spotifyAuthDetails: SpotifyAuthDetails = UserFields.spotifyAuthDetails

    user_id: str = UserFields.user_id

    settings: Settings = UserFields.settings

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }

    def dict(self, *args,**kwargs):
        d = BaseModel.dict(self, *args,**kwargs)
        d.pop('id')
        return d


Users = List[User]

class Test(BaseModel):
    id: Optional[PydanticObjectId] = UserFields.id
    
    def dict(self, *args,**kwargs):
        d = BaseModel.dict(self, *args,**kwargs)
        d.pop('id')
        return d

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }