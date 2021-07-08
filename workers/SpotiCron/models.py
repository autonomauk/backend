from pydantic import BaseModel
from typing import List

class Track(BaseModel):
    id: str

class Tracks(BaseModel):
    tracks: List[Track]

    def __sub__(self,other: List[Track]):
        difference = set([f.id for f in self.tracks]) - set([f.id for f in other.tracks])
        return [Track(id=f) for f in difference]

    def __getitem__(self, item):
        return self.tracks[item]

class Playlist(BaseModel):
    name: str
    id: str = None

Playlists = List[Playlist]
