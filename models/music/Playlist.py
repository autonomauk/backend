from models.ListModel import ListModel
from pydantic import BaseModel
from typing import List

class Playlist(BaseModel):
    name: str
    uri: str = None

    @property
    def id(self):
        if self.uri is not None:
            return self.uri.split(':')[-1]
        else:
            return self.uri

Playlists = list[Playlist]