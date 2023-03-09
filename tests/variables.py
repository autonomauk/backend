from models.music.Track import Tracks
from models.ObjectId import PydanticObjectId
import datetime

from utils.time import get_non_tzaware_time

import json
from bson import json_util

def USER_DICT():
    user: dict = {}
    with open('tests/user.json', 'r') as f:
        user = json.load(f,object_hook=json_util.object_hook)
        user['createdAt'] = user['createdAt'].replace(tzinfo=None)
        user['updatedAt'] = user['updatedAt'].replace(tzinfo=None)
        user['spotifyAuthDetails']['expires_at'] = user['spotifyAuthDetails']['expires_at'].replace(tzinfo=None)

    with open('tests/track_log.json', 'r') as f:
        track_log = json.load(f,object_hook=json_util.object_hook)

        for i in range(len(track_log)):
            track_log[i]['createdAt'] = track_log[i]['createdAt'].replace(tzinfo=None)
            track_log[i]['updatedAt'] = track_log[i]['updatedAt'].replace(tzinfo=None)

        user['track_log'] = track_log

    user['_id'] = PydanticObjectId()

    return user

TRACK_DICT_1 = {'createdAt': get_non_tzaware_time(),
                'updatedAt': get_non_tzaware_time(),
                'name': 'Mr. Brightside',
                'artists': [{
                    'uri': 'spotify:artist:0C0XlULifJtAgn6ZNCW2eu',
                    'name': "The Killers"
                }],
                'album': {
                    'image_url': 'https://i.scdn.co/image/ab67616d0000b2739c284a6855f4945dc5a3cd73',
                    'uri': 'spotify:album:4OHNH3sDzIxnmUADXzv2kT',
                    'name': 'Hot Fuss'
},
    'uri': 'spotify:track:3n3Ppam7vgaVa1iaRUc9Lp'
}

TRACK_DICT_2 = {'createdAt': get_non_tzaware_time(),
                'updatedAt': get_non_tzaware_time(),
                'name': 'Mr. Lightside',
                'artists': [{
                    'uri': 'spotify:artist:AF0XlULifJtAgn6ZNCW2eu',
                    'name': "The Millers"
                }],
                'album': {
                    'image_url': 'https://i.scdn.co/image/de67616d0000b2739c284a6855f4945dc5a3cd73',
                    'uri': 'spotify:album:56HNH3sDzIxnmUADXzv2kT',
                    'name': 'Lotta Fuss'
},
    'uri': 'spotify:track:4m3Ppam7vgaVa1iaRUc9Lp'
}

SPOTIFY_TRACKS_1 = [
    {
        "album": {
            "album_type": "single",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                    },
                    "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                    "id": "6sFIWsNpZYqfjUpaCgueju",
                    "name": "Carly Rae Jepsen",
                    "type": "artist",
                    "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
                }
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/0tGPJ0bkWOUmH7MEOR77qc"
            },
            "href": "https://api.spotify.com/v1/albums/0tGPJ0bkWOUmH7MEOR77qc",
            "id": "0tGPJ0bkWOUmH7MEOR77qc",
            "images": [
                    {
                        "height": 640,
                        "url": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                        "width": 640
                    },
                {
                        "height": 300,
                        "url": "https://i.scdn.co/image/107819f5dc557d5d0a4b216781c6ec1b2f3c5ab2",
                        "width": 300
                    },
                {
                        "height": 64,
                        "url": "https://i.scdn.co/image/5a73a056d0af707b4119a883d87285feda543fbb",
                        "width": 64
                    }
            ],
            "name": "Cut To The Feeling",
            "release_date": "2017-05-26",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:0tGPJ0bkWOUmH7MEOR77qc"
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                },
                "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                "id": "6sFIWsNpZYqfjUpaCgueju",
                "name": "Carly Rae Jepsen",
                "type": "artist",
                "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
            }
        ],
        "disc_number": 1,
        "duration_ms": 207959,
        "explicit": False,
        "external_ids": {
            "isrc": "USUM71703861"
        },
        "external_urls": {
            "spotify": "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl"
        },
        "href": "https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
        "id": "11dFghVXANMlKmJXsNCbNl",
        "is_local": False,
        "name": "Cut To The Feeling",
        "popularity": 63,
        "preview_url": "https://p.scdn.co/mp3-preview/3eb16018c2a700240e9dfb8817b6f2d041f15eb1?cid=774b29d4f13844c495f206cafdad9c86",
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl"
    },
    {
        "album": {
            "album_type": "album",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                    },
                    "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                    "id": "6sFIWsNpZYqfjUpaCgueju",
                    "name": "Carly Rae Jepsen",
                    "type": "artist",
                    "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
                }
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/6SSSF9Y6MiPdQoxqBptrR2"
            },
            "href": "https://api.spotify.com/v1/albums/6SSSF9Y6MiPdQoxqBptrR2",
            "id": "6SSSF9Y6MiPdQoxqBptrR2",
            "images": [
                    {
                        "height": 640,
                        "url": "https://i.scdn.co/image/2fb20bf4c1fb29b503bfc21516ff4b1a334b6372",
                        "width": 640
                    },
                {
                        "height": 300,
                        "url": "https://i.scdn.co/image/a7b076ed5aa0746a21bc71ab7d2b6ed80dd3ebfe",
                        "width": 300
                    },
                {
                        "height": 64,
                        "url": "https://i.scdn.co/image/b1d4c7643cf17c06b967b50623d7d93725b31de5",
                        "width": 64
                    }
            ],
            "name": "Kiss",
            "release_date": "2012-01-01",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:6SSSF9Y6MiPdQoxqBptrR2"
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                },
                "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                "id": "6sFIWsNpZYqfjUpaCgueju",
                "name": "Carly Rae Jepsen",
                "type": "artist",
                "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
            }
        ],
        "disc_number": 1,
        "duration_ms": 193400,
        "explicit": False,
        "external_ids": {
            "isrc": "CAB391100615"
        },
        "external_urls": {
            "spotify": "https://open.spotify.com/track/20I6sIOMTCkB6w7ryavxtO"
        },
        "href": "https://api.spotify.com/v1/tracks/20I6sIOMTCkB6w7ryavxtO",
        "id": "20I6sIOMTCkB6w7ryavxtO",
        "is_local": False,
        "name": "Call Me Maybe",
        "popularity": 74,
        "preview_url": "https://p.scdn.co/mp3-preview/335bede49342352cddd53cc83af582e2240303bb?cid=774b29d4f13844c495f206cafdad9c86",
        "track_number": 3,
        "type": "track",
        "uri": "spotify:track:20I6sIOMTCkB6w7ryavxtO"
    },
    {
        "album": {
            "album_type": "album",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                    },
                    "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                    "id": "6sFIWsNpZYqfjUpaCgueju",
                    "name": "Carly Rae Jepsen",
                    "type": "artist",
                    "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
                }
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/1DFixLWuPkv3KT3TnV35m3"
            },
            "href": "https://api.spotify.com/v1/albums/1DFixLWuPkv3KT3TnV35m3",
            "id": "1DFixLWuPkv3KT3TnV35m3",
            "images": [
                    {
                        "height": 640,
                        "url": "https://i.scdn.co/image/3f65c5400c7f24541bfd48e60f646e6af4d6c666",
                        "width": 640
                    },
                {
                        "height": 300,
                        "url": "https://i.scdn.co/image/ff347680d9e62ccc144926377d4769b02a1024dc",
                        "width": 300
                    },
                {
                        "height": 64,
                        "url": "https://i.scdn.co/image/c836e14a8ceca89e18012cab295f58ceeba72594",
                        "width": 64
                    }
            ],
            "name": "Emotion (Deluxe)",
            "release_date": "2015-09-18",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:1DFixLWuPkv3KT3TnV35m3"
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
                },
                "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
                "id": "6sFIWsNpZYqfjUpaCgueju",
                "name": "Carly Rae Jepsen",
                "type": "artist",
                "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
            }
        ],
        "disc_number": 1,
        "duration_ms": 251319,
        "explicit": False,
        "external_ids": {
            "isrc": "USUM71507009"
        },
        "external_urls": {
            "spotify": "https://open.spotify.com/track/7xGfFoTpQ2E7fRF5lN10tr"
        },
        "href": "https://api.spotify.com/v1/tracks/7xGfFoTpQ2E7fRF5lN10tr",
        "id": "7xGfFoTpQ2E7fRF5lN10tr",
        "is_local": False,
        "name": "Run Away With Me",
        "popularity": 50,
        "preview_url": "https://p.scdn.co/mp3-preview/3e05f5ed147ca075c7ae77c01f2cc0e14cfad78d?cid=774b29d4f13844c495f206cafdad9c86",
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:7xGfFoTpQ2E7fRF5lN10tr"
    }
]

SPOTIFY_PLAYLIST_1 = {
    "collaborative": False,
    "description": "Having friends over for dinner? Here´s the perfect playlist.",
    "external_urls": {
        "spotify": "http://open.spotify.com/user/spotify/playlist/59ZbFPES4DQwEjBpWHzrtC"
    },
    "followers": {
        "href": None,
        "total": 143350
    },
    "href": "https://api.spotify.com/v1/users/spotify/playlists/59ZbFPES4DQwEjBpWHzrtC",
    "id": "59ZbFPES4DQwEjBpWHzrtC",
    "images": [
        {
            "url": "https://i.scdn.co/image/68b6a65573a55095e9c0c0c33a274b18e0422736"
        }
    ],
    "name": "Dinner with Friends",
    "owner": {
        "external_urls": {
            "spotify": "http://open.spotify.com/user/spotify"
        },
        "href": "https://api.spotify.com/v1/users/spotify",
        "id": "spotify",
        "type": "user",
        "uri": "spotify:user:spotify"
    },
    "public": None,
    "snapshot_id": "bNLWdmhh+HDsbHzhckXeDC0uyKyg4FjPI/KEsKjAE526usnz2LxwgyBoMShVL+z+",
    "tracks": {
        "href": "https://api.spotify.com/v1/users/spotify/playlists/59ZbFPES4DQwEjBpWHzrtC/tracks",
        "items": [
            {
                "added_at": "2014-09-01T04:21:28Z",
                "added_by": {
                    "external_urls": {
                        "spotify": "http://open.spotify.com/user/spotify"
                    },
                    "href": "https://api.spotify.com/v1/users/spotify",
                    "id": "spotify",
                    "type": "user",
                    "uri": "spotify:user:spotify"
                },
                "is_local": False,
                "track": {
                    "album": {
                        "album_type": "single",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/album/5GWoXPsTQylMuaZ84PC563"
                        },
                        "href": "https://api.spotify.com/v1/albums/5GWoXPsTQylMuaZ84PC563",
                        "id": "5GWoXPsTQylMuaZ84PC563",
                        "images": [
                            {
                                "height": 640,
                                "url": "https://i.scdn.co/image/47421900e7534789603de84c03a40a826c058e45",
                                "width": 640
                            },
                            {
                                "height": 300,
                                "url": "https://i.scdn.co/image/0d447b6faae870f890dc5780cc58d9afdbc36a1d",
                                "width": 300
                            },
                            {
                                "height": 64,
                                "url": "https://i.scdn.co/image/d926b3e5f435ef3ac0874b1ff1571cf675b3ef3b",
                                "width": 64
                            }
                        ],
                        "name": "I''m Not The Only One",
                        "type": "album",
                        "uri": "spotify:album:5GWoXPsTQylMuaZ84PC563"
                    },
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/2wY79sveU1sp5g7SokKOiI"
                            },
                            "href": "https://api.spotify.com/v1/artists/2wY79sveU1sp5g7SokKOiI",
                            "id": "2wY79sveU1sp5g7SokKOiI",
                            "name": "Sam Smith",
                            "type": "artist",
                            "uri": "spotify:artist:2wY79sveU1sp5g7SokKOiI"
                        }
                    ],
                    "disc_number": 1,
                    "duration_ms": 204732,
                    "explicit": False,
                    "external_ids": {
                        "isrc": "GBUM71403920"
                    },
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/4i9sYtSIlR80bxje5B3rUb"
                    },
                    "href": "https://api.spotify.com/v1/tracks/4i9sYtSIlR80bxje5B3rUb",
                    "id": "4i9sYtSIlR80bxje5B3rUb",
                    "name": "I''m Not The Only One - Radio Edit",
                    "popularity": 45,
                    "preview_url": "https://p.scdn.co/mp3-preview/dd64cca26c69e93ea78f1fff2cc4889396bb6d2f",
                    "track_number": 1,
                    "type": "track",
                    "uri": "spotify:track:4i9sYtSIlR80bxje5B3rUb"
                }
            }
        ],
        "limit": 100,
        "next": "https://api.spotify.com/v1/users/spotify/playlists/59ZbFPES4DQwEjBpWHzrtC/tracks?offset=100&limit=100",
        "offset": 0,
        "previous": None,
        "total": 105
    },
    "type": "playlist",
    "uri": "spotify:user:spotify:playlist:59ZbFPES4DQwEjBpWHzrtC"
}