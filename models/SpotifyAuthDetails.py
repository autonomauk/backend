from os import access
from typing import Any
import utils
from pydantic import BaseModel
from pydantic.fields import Field

class SpotifyAuthDetailsFields:
    
    access_token = Field(description="Access token")

    refresh_token = Field(description="Refresh token")

    expires_in = Field(description="Expires in X seconds")

    expires_at = Field(-1,description="Expires at")
 

    token_type = Field(description='Token type')

class SpotifyAuthDetails(BaseModel):    
    access_token: str = SpotifyAuthDetailsFields.access_token

    refresh_token: str = SpotifyAuthDetailsFields.refresh_token

    expires_in: int = SpotifyAuthDetailsFields.expires_in

    expires_at: int = SpotifyAuthDetailsFields.expires_at

    token_type: str = SpotifyAuthDetailsFields.token_type