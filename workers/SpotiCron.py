from logging import info
import dateutil.parser
import datetime
import time

from pydantic.types import conset

from models.SpotifyAuthDetails import SpotifyAuthDetails
from typing import List

from spotipy.exceptions import SpotifyException
from repositories.user import UserRepository
from models.User import User, Users
import spotipy

from config import *

from pydantic import BaseModel

import schedule

from loguru import logger
import sys

logger.configure(**{
    "handlers": [
        {"sink": sys.stderr, "format": "UP {elapsed} | <level>{level: <8}</level> | PID {process} | <cyan>{file}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"}
    ]})


class Track(BaseModel):
    id: str


Tracks = List[Track]


class Playlist(BaseModel):
    name: str
    id: str = None


Playlists = List[Playlist]

spotify_oauth = spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)


def SpotiCronRunner():
    playlist_name = time.strftime('%B %y', time.localtime())

    users: Users = UserRepository.list()

    for user in users:
        try:
            SpotiCronPerUser(user, playlist_name)
        except SpotifyException as e:
            if e.msg.find("The access token expired"):
                SpotiCronPerUser(user, playlist_name)


@logger.catch
def SpotiCronPerUser(user: User, playlist_name: str):
    target_playlist: Playlist = Playlist(name=playlist_name)
    
    if spotify_oauth.is_token_expired(user.spotifyAuthDetails.dict()):
        logger.debug(f"Refreshing access token for {user.id}")
        token_info = spotify_oauth.refresh_access_token(
            user.spotifyAuthDetails.refresh_token)

        user.spotifyAuthDetails = SpotifyAuthDetails(**token_info)
        UserRepository.update(user.id, user)

    spotify = spotipy.Spotify(user.spotifyAuthDetails.access_token)

    # Try to find playlist
    playlists: Playlists = []
    limit = 50
    offset = 0
    total = None
    while True:
        playlists = spotify.current_user_playlists(
            limit=limit, offset=offset)
        total = playlists['total']
        playlists: Playlists = [Playlist(**document)
                                for document in playlists['items']]

        for playlist in playlists:
            if playlist.name == target_playlist.name:
                target_playlist.id = playlist.id

        if target_playlist.id is not None:
            break
        elif offset < total:
            offset += limit
        else:
            # Create playlist
            playlist = spotify.user_playlist_create(
                user.user_id,
                target_playlist.name,
                public=True,
                collaborative=False,
                description=f"Playlist created by {SP_WEBSITE}"
            )
            break

    # Find all saved tracks for this month
    # TODO: Compare with playlist's current songs or even "last checked"
    saved_tracks: Tracks = []
    today: datetime.date = datetime.date.today()
    while True:
        more_to_add = True
        for item in spotify.current_user_saved_tracks(limit=limit, offset=offset)['items']:
            added_at = dateutil.parser.parse(item['added_at'])
            # TODO Change logic for different playlist schema
            if added_at.month == today.month and added_at.year == today.year:
                saved_tracks.append(Track(**item['track']))
            else:
                more_to_add = False
        if not more_to_add:
            break

    tracks_in_playlist: Tracks = []
    limit = 100
    offset = 0
    total = None
    while True:
        result = spotify.playlist_tracks(
            target_playlist.id,
            limit=limit,
            offset=offset)
        total = result['total']

        for item in result['items']:
            item = item['track']
            tracks_in_playlist.append(Track(**item))

        if offset < total:
            offset += limit
        else:
            break

    tracks_to_add: Tracks = [Track(id=g) for g in
                             # Difference in sets
                             set([f.id for f in saved_tracks]) - \
                             set([f.id for f in tracks_in_playlist])
                             ]

    if len(tracks_to_add) > 0:
        logger.info(
            f"{len(tracks_to_add)} track{'s' if len(tracks_to_add) > 1 else ''} to add for user {user.id}")
        spotify.playlist_add_items(
            target_playlist.id, [track.id for track in tracks_to_add])
    else:
        logger.debug(f"No tracks to add for user {user.id}")

def SpotiCron():
    logger.info("Starting SpotiCron.py")
    schedule.every(3).minutes.do(SpotiCronRunner)

    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("Exiting SpotiCron.py")