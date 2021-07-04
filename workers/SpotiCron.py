import datetime
from functools import lru_cache
import time
from typing import List
import dateutil.parser

import schedule
from loguru import logger

from pydantic import BaseModel, validator

from spotipy.exceptions import SpotifyException
import spotipy

from repositories.stats import StatsRepository
from repositories.user import UserRepository
from models.SpotifyAuthDetails import SpotifyAuthDetails
from models.User import User, Users
from models.Stats import RunTimeStat
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SP_WEBSITE
from utils.time import get_time


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

spotify_oauth = spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI)

# Over-write the original function to track our Spotify API requests

# pylint:disable=protected-access
orig_func = spotipy.Spotify._internal_call


def wrapper(*args, **kwargs):
    StatsRepository.spotify_request_called()
    return orig_func(*args, **kwargs)


spotipy.Spotify._internal_call = wrapper
# pylint:enable=protected-access


def SpotiCronRunner():
    t = time.time()
    playlist_name = time.strftime('%B %y', time.localtime())

    users: Users = UserRepository.list()

    logger.debug(f"Start of SpotiCronRunner with {len(users)} users")

    for user in users:
        logger.debug(f"Running for {user.id=}")
        try:
            SpotiCronRunnerPerUser(user, playlist_name).run()
        except SpotifyException as e:
            if e.msg.find("The access token expired"):
                SpotiCronRunnerPerUser(user, playlist_name).run()
    run_time = RunTimeStat(time=time.time()-t)
    StatsRepository.spoticron_run_time(run_time)
    logger.debug(f"End of SpotiCronRunner after {run_time.time:.2f}s")


class SpotiCronRunnerPerUser:

    def __init__(self, user: User, playlist_name: str) -> None:
        self.user: User = user
        self.target_playlist: Playlist = Playlist(name=playlist_name)

        if spotify_oauth.is_token_expired(self.user.spotifyAuthDetails.to_spotipy_dict()):
            logger.debug(f"Refreshing access token for {self.user.id}")
            token_info = spotify_oauth.refresh_access_token(
                self.user.spotifyAuthDetails.refresh_token)

            self.user.spotifyAuthDetails = SpotifyAuthDetails(**token_info)
            UserRepository.update(self.user.id, self.user)

        self.spotify = spotipy.Spotify(
            self.user.spotifyAuthDetails.access_token,
            requests_timeout=40)

    @logger.catch
    def run(self):
        # Updates self.target_playlist
        self.target_playlist = self.find_playlist()

        # Find all saved tracks for this month
        tracks_saved = self.find_saved_tracks_filtered()
        tracks_in_playlist = self.find_songs_in_target_playlist()

        tracks_to_add: Tracks = Tracks(tracks_saved) - Tracks(tracks_in_playlist)

        if len(tracks_to_add) > 0:
            logger.info(
                f"{len(tracks_to_add)} track{'s' if len(tracks_to_add) > 1 else ''}" +
                " to add for user {user.id}")
            self.spotify.playlist_add_items(
                self.target_playlist.id, [track.id for track in tracks_to_add])
        else:
            logger.debug(f"No tracks to add for user {self.user.id}")

    def find_playlist(self) -> Playlist:
        # Try to find playlist
        playlists: Playlists = []
        limit = 50
        offset = 0
        total = None
        while True:
            playlists = self.spotify.current_user_playlists(
                limit=limit, offset=offset)
            total = playlists['total']
            playlists: Playlists = [Playlist(**document)
                                    for document in playlists['items']]

            for playlist in playlists:
                if playlist.name == self.target_playlist.name:
                    return playlist


            if offset < total:
                offset += limit
            else:
                return self.create_playlist_for_user()

    def create_playlist_for_user(self) -> Playlist:
        # Create playlist
        res = self.spotify.user_playlist_create(
            self.user.user_id,
            self.target_playlist.name,
            public=True,
            collaborative=False,
            description=f"Playlist created by {SP_WEBSITE}"
        )

        return Playlist(name=res['name'],id=res['id'])

    def find_saved_tracks_filtered(self) -> Tracks:
        # TODO: Compare with playlist's current songs or even "last checked"
        limit = 50
        offset = 0
        saved_tracks: Tracks = []
        while True:
            for item in self.spotify.current_user_saved_tracks(limit=limit, offset=offset)['items']:
                added_at = dateutil.parser.parse(item['added_at'])

                # TODO Change logic for different playlist schema
                if TrackFilter.monthly(added_at):
                    saved_tracks.append(Track(**item['track']))
                else:
                    return saved_tracks

    def find_songs_in_target_playlist(self):
        tracks_in_playlist: Tracks = []
        limit = 100
        offset = 0
        total = None
        while True:
            result = self.spotify.playlist_tracks(
                self.target_playlist.id,
                limit=limit,
                offset=offset)
            total = result['total']

            for item in result['items']:
                item = item['track']
                tracks_in_playlist.append(Track(**item))

            if offset < total:
                offset += limit
            else:
                return tracks_in_playlist

class TrackFilter:
    @classmethod
    def monthly(cls, date: datetime.datetime) -> bool:
        assert isinstance(date, (datetime.date,datetime.datetime))
        now = cls.now()
        return date.month == now.month and date.year == now.year

    @staticmethod
    @lru_cache(maxsize=1)
    def now() -> datetime.datetime:
        return get_time()



def SpotiCron():
    logger.info("Starting SpotiCron.py")
    schedule.every(3).minutes.do(SpotiCronRunner())

    SpotiCronRunner()
    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("Exiting SpotiCron.py")
