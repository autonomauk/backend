from models.SpotifyAuthDetails import SpotifyAuthDetails
import pytest
import datetime


STATIC_SAD_DICT = {
        "access_token": "BQCXEA-w453XFLYHJRc7ekgTSgfS5zoJMPS484NWoqupGuZz4xdtsS75t6ykvvy38Ww-bo42q5oGKIl4wWLcbptoB2zr7CUwl-7bXUgErcvxwaY8u3vl6im5s62oBzGAG7IOe3LoX2PdydJCaOrrTLKfwuwjNv2kQ3A-NMwLBzdYZJronCOw2At6pRa6CLFfriibOQXJyMxzzDXOos_mZjYwsNDWbY8BvNrpNhopFfnT",
        "refresh_token": "AQALYnPy0bgykbbcudCVZ0AbyAIWLN6mXregSmMSjnmzAjjHUiKqxfBKGTwrsBUo3bVCRcXwO7u0srC5FII6zphK4aXxCUDlYmMk3Yuy6G95pIZyTYFeo-CdFE8W85Pb-Os",
        "expires_in":  "3600",
        "expires_at":  datetime.datetime.fromtimestamp(1625166513000/1000),
        "token_type": "Bearer"       
}

@pytest.fixture
def spotifyAuthDetails():
    yield SpotifyAuthDetails(**STATIC_SAD_DICT)

class TestSpotifyAuthDetails:
    def test_to_spotipy_dict_func(self,spotifyAuthDetails):
        spotifyAuthDetailsDict: dict = spotifyAuthDetails.to_spotipy_dict()
        spotifyAuthDetailsKeys: list = spotifyAuthDetailsDict.keys()
        
        assert isinstance(spotifyAuthDetailsDict["expires_at"],(int, float))
        assert spotifyAuthDetailsDict["expires_at"] == spotifyAuthDetails.expires_at.timestamp()

        for f in STATIC_SAD_DICT.keys():
            assert f in spotifyAuthDetailsKeys