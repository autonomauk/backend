import functools
from models.music.TrackLog import TrackLog
import time
from utils.time import get_non_tzaware_time
from utils.logger import timeit
import dateutil.parser
import copy

import schedule
from loguru import logger

from spotipy.exceptions import SpotifyException
import spotipy

from repositories.stats import StatsRepository
from repositories.user import UserRepository
from models.SpotifyAuthDetails import SpotifyAuthDetails
from models.User import User, Users
from models.Stats import RunTimeStat
from models.music import Track, Tracks, Playlist, Playlists
from config import settings
from prometheus_client import start_http_server

from .filter import TrackFilter

import concurrent.futures

spotify_oauth = spotipy.oauth2.SpotifyOAuth(
    client_id=settings.spotify.CLIENT_ID,
    client_secret=settings.spotify.CLIENT_SECRET,
    redirect_uri=settings.spotify.REDIRECT_URI)

# Over-write the original function to track our Spotify API requests
# pylint:disable=protected-access
orig_func = spotipy.Spotify._internal_call


def wrapper(*args, **kwargs):
    StatsRepository.spotify_request_called()
    return orig_func(*args, **kwargs)


spotipy.Spotify._internal_call = wrapper
# pylint:enable=protected-access


@timeit
def SpotiCronRunner(threaded: bool = True):
    playlist_name = time.strftime('%B %y', time.localtime())

    users: Users = UserRepository.list({"settings.enabled": True})
    if threaded:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(lambda x: SpotiCronRunnerPerUser(
                user=x, playlist_name=playlist_name).run(), users)
    else:
        for user in users:
            SpotiCronRunnerPerUser(user, playlist_name).run()


class SpotiCronRunnerPerUser:
    def __init__(self, user: User, playlist_name: str) -> None:
        self._t1 = time.time()

        self.log = logger.bind(user_id=str(user.id))
        self.log.debug(f"Start for {user.user_id}")

        self.user: User = user
        self.target_playlist: Playlist = Playlist(name=playlist_name)

        if self.user.spotifyAuthDetails.expires_at < get_non_tzaware_time():
            self.reauthorize()

        self.spotify = spotipy.Spotify(
            self.user.spotifyAuthDetails.access_token,
            requests_timeout=40)

    def rerun_on_token_expire(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SpotifyException as e:
                if e.msg.find("The access token expired"):
                    args[0].reauthorize()
                    return func(*args, **kwargs)
        return wrapper

    def __del__(self):
        self._dt = time.time()-self._t1
        StatsRepository.spoticron_run()
        StatsRepository.spoticron_run_time(RunTimeStat(time=self._dt))
        self.log.debug(f"End in {self._dt:.3f}s")

    def reauthorize(self):
        self.log.debug(
            f"Refreshing access token ({self.user.spotifyAuthDetails.access_token:16.16}...)")

        token_info = spotify_oauth.refresh_access_token(
            self.user.spotifyAuthDetails.refresh_token)

        self.user.spotifyAuthDetails = SpotifyAuthDetails(**token_info)
        UserRepository.update(self.user.id, self.user)

        self.log.debug(
            f"Access token refreshed ({self.user.spotifyAuthDetails.access_token:16.16}...)")

    @rerun_on_token_expire
    def run(self) -> bool:
        # Find all saved tracks for this month
        tracks_saved = self.find_saved_tracks_filtered()
        if len(tracks_saved) == 0:
            self.log.debug("No tracks to add")
            return False

        # Updates self.target_playlist
        self.target_playlist = self.find_playlist()

        if self.target_playlist is None:
            self.target_playlist = self.create_playlist_for_user()
            tracks_in_playlist = []
        else:
            tracks_in_playlist = self.find_songs_in_target_playlist()

        diff = set([f.uri for f in tracks_saved]) - \
            set([f.uri for f in tracks_in_playlist])
        tracks_to_add: Tracks = Tracks(
            [f for f in tracks_saved if f.uri in diff])

        self.log.info(
            f"{len(tracks_to_add)} track{'s' if len(tracks_to_add) > 1 else ''} to add")

        self.spotify.playlist_add_items(
            self.target_playlist.id, [track.uri for track in tracks_to_add])

        StatsRepository.spoticron_tracks_added(
            len(tracks_to_add), id=self.user.id)
        UserRepository.add_tracks_to_log(self.user.id, [TrackLog(
            track=f, playlist=self.target_playlist) for f in tracks_to_add])
        return True

    @timeit
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
                    self.target_playlist = copy.deepcopy(playlist)
                    return self.target_playlist

            if offset < total:
                offset += limit
            else:
                return None

    @timeit
    def create_playlist_for_user(self) -> Playlist:
        # Create playlist
        res = self.spotify.user_playlist_create(
            self.user.user_id,
            self.target_playlist.name,
            public=True,
            collaborative=False,
            description=f"Playlist created by {settings.server.url}"
        )
        return Playlist(**res)

    @timeit
    def find_saved_tracks_filtered(self) -> Tracks:
        # TODO: Compare with playlist's current songs or even "last checked"
        limit = 50
        offset = 0
        saved_tracks: list[Track] = []
        while True:
            self.log.trace(
                f"Finding saved tracks ({limit=}, {offset=}, {len(saved_tracks)=})")

            current_user_saved_tracks: list = self.spotify.current_user_saved_tracks(
                limit=limit,
                offset=offset
            )['items']

            if len(current_user_saved_tracks) == 0:
                return saved_tracks

            for item in current_user_saved_tracks:
                added_at = dateutil.parser.parse(item['added_at'])
                self.log.trace(f"Song was added at {added_at}")

                # TODO Change logic for different playlist schema
                if TrackFilter.monthly(added_at):
                    saved_tracks.append(
                        Track.from_spotify_object(item['track']))
                else:
                    self.log.trace(f"Found {len(saved_tracks)} saved tracks")
                    return Tracks(saved_tracks)

            offset += limit

    @timeit
    def find_songs_in_target_playlist(self) -> Tracks:
        self.log.trace(
            f"Finding songs in target playlist {self.target_playlist.name}")
        tracks_in_playlist: list[Track] = []
        limit = 100
        offset = 0
        total = None
        while True:
            result = self.spotify.playlist_items(
                playlist_id=self.target_playlist.id,
                limit=limit,
                offset=offset)
            total = result['total']

            for item in result['items']:
                tracks_in_playlist.append(
                    Track.from_spotify_object(item['track']))

            if offset < total:
                offset += limit
            else:
                self.log.trace(
                    f"Found {len(tracks_in_playlist)} songs in target playlist")
                return Tracks(tracks_in_playlist)


def SpotiCron(
    profile: bool = False,
    oneshot: bool = False,
    threaded: bool = True,
    dev: bool = True
        ):

    if profile:
        logger.info("Starting SpotiCron with profiling (one-shot)")
        import cProfile
        from pstats import Stats
        profiler = cProfile.Profile()
        profiler.enable()
    else:
        logger.info("Starting SpotiCron")

    SpotiCronRunner(threaded=threaded)
    if not oneshot:
        scheduler = schedule.every(5).minutes
        if dev:
            scheduler = schedule.every(10).seconds
        scheduler.do(lambda: SpotiCronRunner(threaded=threaded))
        start_http_server(8024)
        while True:
            schedule.run_pending()
            time.sleep(1)

    if profile:
        profiler.disable()

        stats = Stats(profiler).sort_stats('tottime')
        stats.print_stats()
        stats.dump_stats('profiling_stats.txt')

    logger.info("Exiting SpotiCron.py")
