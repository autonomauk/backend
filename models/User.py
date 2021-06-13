from typing import List, Optional
from models.SpotifyAuthDetails import SpotifyAuthDetailsFields,SpotifyAuthDetails
from os import access
from pydantic import BaseModel
from pydantic.fields import Field

_string = dict(min_length=1)

class UserFields:
    id = Field(
        description="UUID fo user",
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

class UserBaseModel(BaseModel):
    id: Optional[str] = UserFields.id

class User(UserBaseModel):
    
    spotifyAuthDetails: SpotifyAuthDetails = UserFields.spotifyAuthDetails

    user_id: str = UserFields.user_id

Users = List[User]