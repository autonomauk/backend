import datetime
import inspect

from starlette.responses import RedirectResponse
from fastapi import status as statuscode
import pytest

from repositories.exceptions import (AuthenticationFailureException, 
                                    SpotifyAuthenticationFailureException)
from repositories.auth_flow import AuthFlowRepository
from models.ObjectId import PydanticObjectId
from models.User import User
from models.JWToken import JWToken
import config

STATIC_USER_DICT = {
    "_id": str(PydanticObjectId()),
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

# pylint: disable=redefined-outer-name
@pytest.fixture
def user():
    yield User(**STATIC_USER_DICT)

JWT_SIGNED_WTIH_FOREIGN_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwZTFkODU4ODA5MTI1MDg4MmYwM2QyMiIsImV4cCI6MTYyNTUwMDE2NX0.Om6p1ADU8kTOlYS8P2pTb0k9oGuEj45ZJJdhtdvCuKQ"
JWT_WITHOUT_ID = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.CV_sYj7xzNERRCn3jh2wOI5-tx_oyZX5gOUphkYTuks"
JWT_VALID_BUT_TIMED_OUT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwZTFkYjhlOTgxYzRjNWE4ZTgxOTllNCIsImV4cCI6MTYyNTUwMDk0Mn0.hr9_No4G5aBO_Grcg36C8KH1XyU-GpH566TOlM9r4Oc"

class TestAuthFlowRepository:
    def test_jtw_flow(self, user: User):
        jwt: JWToken = AuthFlowRepository.create_JWT(user)

        decrypted_user_id = AuthFlowRepository.validate_JWT(jwt_str=jwt.access_token)

        assert decrypted_user_id == str(user.id)

        for token in [JWT_SIGNED_WTIH_FOREIGN_KEY, JWT_WITHOUT_ID, JWT_VALID_BUT_TIMED_OUT]:
            with pytest.raises(AuthenticationFailureException):
                AuthFlowRepository.validate_JWT(jwt_str=token)

    def test_auth_required(self, user: User):
        jwt: JWToken = AuthFlowRepository.create_JWT(user)

        # pylint:disable=unexpected-keyword-arg
        # pylint:disable=function-redefined

        # No normal args
        @AuthFlowRepository.auth_required_wrapper
        def handler():
            return 1

        args = inspect.signature(handler).parameters

        assert "jwt" in args
        assert len(args) == 1

        with pytest.raises(AuthenticationFailureException):
            handler()

        assert handler(jwt=jwt.access_token) == 1

        # 1 normal arg
        @AuthFlowRepository.auth_required_wrapper
        def handler(x):
            return x

        args = inspect.signature(handler).parameters

        assert "jwt" in args
        assert len(args) == 2

        with pytest.raises(AuthenticationFailureException):
            handler(1)

        assert handler(x=2, jwt=jwt.access_token) == 2

        # JWT already as arg
        @AuthFlowRepository.auth_required_wrapper
        def handler(jwt):
            return jwt

        args = inspect.signature(handler).parameters

        assert "jwt" in args
        assert len(args) == 1

        with pytest.raises(AuthenticationFailureException):
            handler(jwt=1)
        with pytest.raises(AuthenticationFailureException):
            handler(jwt=None)

        assert handler(jwt=jwt.access_token) == jwt.access_token

    def test_login(self):
        rr: RedirectResponse = AuthFlowRepository.login()

        assert isinstance(rr, RedirectResponse)
        assert rr.status_code == statuscode.HTTP_307_TEMPORARY_REDIRECT

        url: str = rr.headers['location']

        assert "accounts.spotify.com/authorize" in url
        assert config.SPOTIFY_CLIENT_ID in url
        assert config.SPOTIFY_REDIRECT_URI in url
        assert "+".join(config.SPOTIFY_SCOPE.split()) in url

    def test_login_callback(self):
        with pytest.raises(SpotifyAuthenticationFailureException):
            AuthFlowRepository.login_callback("spotify_basic_token_that_wont_work")