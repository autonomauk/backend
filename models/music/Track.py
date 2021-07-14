from typing import Any, List

from pydantic.fields import Field
from pydantic.main import BaseModel
from models.music import Album
from models.music import Artist
from models.TimedBaseModel import TimedBaseModel

class Track(TimedBaseModel):
    name: str = Field(..., example="Mr. Brightside")
    artists: list[Artist]
    album: Album
    uri: str = Field(...,example="spotify:track:3n3Ppam7vgaVa1iaRUc9Lp")

    @classmethod
    def from_spotify_object(cls, spotify_object):
        artists = [Artist.from_spotify_object(f) for f in spotify_object['artists']]
        album = Album.from_spotify_object(spotify_object['album'])

        track = {'name':spotify_object['name'],'uri':spotify_object['uri'],'artists':artists, 'album':album}

        return cls(**track)

Tracks = list[Track]
