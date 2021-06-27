from models.Settings import Settings
from typing import List, Optional, Set
from models.SpotifyAuthDetails import SpotifyAuthDetailsFields,SpotifyAuthDetails
from os import access
from pydantic import BaseModel
from pydantic.fields import Field

_string = dict(min_length=1)

class UserFields:
    id = Field(
        description="UUID for user",
        type=Optional[str],
        **_string
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

class UserBaseModel(BaseModel):
    id: Optional[str] = UserFields.id

class User(UserBaseModel):
    
    spotifyAuthDetails: SpotifyAuthDetails = UserFields.spotifyAuthDetails

    user_id: str = UserFields.user_id

    settings: Settings = UserFields.settings

Users = List[User]