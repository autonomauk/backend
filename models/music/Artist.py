from pydantic import BaseModel
from pydantic.fields import Field

class Artist(BaseModel):
    uri: str = Field(...,example="spotify:artist:0C0XlULifJtAgn6ZNCW2eu")
    name: str = Field(...,example="The Killers")

    @classmethod
    def from_spotify_object(cls, spotify_object):
        artist = {'name':spotify_object['name'],'uri':spotify_object['uri']}
        return cls(**artist)