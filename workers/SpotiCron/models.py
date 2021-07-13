from pydantic import BaseModel
from typing import List

class Playlist(BaseModel):
    name: str
    id: str = None

Playlists = List[Playlist]
