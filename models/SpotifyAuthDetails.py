from os import access
from pydantic import BaseModel
from pydantic.fields import Field

class SpotifyAuthDetailsFields:
    
    access_token = Field(description="Access token")

    refresh_token = Field(description="Refresh token")
 

class SpotifyAuthDetails(BaseModel):
    
    access_token: str = SpotifyAuthDetailsFields.access_token

    refresh_token: str = SpotifyAuthDetailsFields.refresh_token