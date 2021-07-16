from pydantic import BaseModel
from pydantic.fields import Field

class Album(BaseModel):
    image_url: str = Field(..., example="https://i.scdn.co/image/ab67616d0000b2739c284a6855f4945dc5a3cd73")
    uri: str = Field(..., example="spotify:album:4OHNH3sDzIxnmUADXzv2kT")
    name: str = Field(..., example="Hot Fuss")

    @classmethod
    def from_spotify_object(cls, spotify_object):
        album = {'name':spotify_object['name'],'image_url': spotify_object['images'][0]['url'], 'uri':spotify_object['uri'] }
        return cls(**album)