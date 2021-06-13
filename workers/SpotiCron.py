from typing import List

from spotipy.exceptions import SpotifyException
from repositories.user import UserRepository
from models.User import User, Users
import spotipy

from config import *

from pydantic import BaseModel
import time

class Track(BaseModel):
    id:str 
    uri:str

Tracks = List[Track]

class Playlist(BaseModel):
    name:str
    id:str
    uri:str

Playlists = List[Playlist]

def RefreshAndRepeatIfRequired(func):
    def handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SpotifyException as e:
            if e.msg.find("The access token expired") and any([isinstance(f,User) for f in args]):
                user = [f for f in args if isinstance(f, User)][0]
                spotify = spotipy.Spotify(user.spotifyAuthDetails.access_token)
                https://stackoverflow.com/questions/49239516/spotipy-refreshing-a-token-with-authorization-code-flow
                spotify.oauth_manager.refresh_access_token(user.spotifyAuthDetails.refresh_token)


    return handler


def SpotiCronRunner():
    playlist_name = time.strftime('%B %y', time.localtime())
    users: Users = UserRepository.list()
    
    user: User = users[0]

    SpotiCronPerUser(user)

@RefreshAndRepeatIfRequired     
def SpotiCronPerUser(user: User):
    spotify = spotipy.Spotify(user.spotifyAuthDetails.access_token)
    
    playlists = []
    while True:
        limit = 50
        offset = 0
        while True:
            playlists = spotify.current_user_playlists(limit=limit,offset=offset)
            playlists = [Playlist(**document) for document in  playlists['items']]



        tracks = spotify.current_user_saved_tracks(limit=limit,offset=offset)
        tracks: Tracks = [Track(**document['track']) for document in tracks['items']]




if __name__ == "__main__":
    SpotiCronRunner()