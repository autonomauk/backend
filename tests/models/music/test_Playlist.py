from tests.variables import SPOTIFY_PLAYLIST_1
from models.music import Playlist, Playlists

class TestPlaylist:
    def test_playlist(self):
        playlist: Playlist = Playlist(**SPOTIFY_PLAYLIST_1)

        assert playlist.name == SPOTIFY_PLAYLIST_1['name']
        assert playlist.id == SPOTIFY_PLAYLIST_1['id']
        assert playlist.uri == SPOTIFY_PLAYLIST_1['uri']


        playlist = Playlist(name="no_uri")
        assert playlist.name == "no_uri"
        assert playlist.id is None
        assert playlist.uri is None