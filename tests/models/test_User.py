from models.User import User
import datetime
import pytest


STATIC_USER_DICT = {
    "_id": "60ddaca8350481c30cfc2a94",
    "createdAt": datetime.datetime.fromtimestamp(1625140392353/1000),
    "updatedAt": datetime.datetime.fromtimestamp(1625162913532/1000),
    "spotifyAuthDetails": {
        "access_token": "BQCXEA-w453XFLYHJRc7ekgTSgfS5zoJMPS484NWoqupGuZz4xdtsS75t6ykvvy38Ww-bo42q5oGKIl4wWLcbptoB2zr7CUwl-7bXUgErcvxwaY8u3vl6im5s62oBzGAG7IOe3LoX2PdydJCaOrrTLKfwuwjNv2kQ3A-NMwLBzdYZJronCOw2At6pRa6CLFfriibOQXJyMxzzDXOos_mZjYwsNDWbY8BvNrpNhopFfnT",
        "refresh_token": "AQALYnPy0bgykbbcudCVZ0AbyAIWLN6mXregSmMSjnmzAjjHUiKqxfBKGTwrsBUo3bVCRcXwO7u0srC5FII6zphK4aXxCUDlYmMk3Yuy6G95pIZyTYFeo-CdFE8W85Pb-Os",
        "expires_in":  "3600",
        "expires_at":  datetime.datetime.fromtimestamp(1625166513000/1000),
        "token_type": "Bearer"
    },
    "user_id": "iwishiwasaneagle",
    "settings": {
        "PlaylistNamingScheme": "MONTHLY"
    }
}


@pytest.fixture()
def user():
    yield User(**STATIC_USER_DICT)


class TestUser:
    def test_dict_func(self, user: User):
        user_dict: dict = user.dict()
        user_dict_keys: list = user_dict.keys()

        assert "id" not in user_dict_keys

        STATIC_USER_DICT.pop('_id')
        for f in STATIC_USER_DICT.keys():
            assert f in user_dict_keys