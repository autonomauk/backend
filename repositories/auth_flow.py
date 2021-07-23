from os import stat
from models.ObjectId import PydanticObjectId
from urllib3.response import HTTPResponse
import utils
from fastapi import Header
from datetime import timedelta,datetime
from starlette.responses import RedirectResponse
import inspect

from config import *
from loguru import logger

from models.JWToken import JWToken
from models.User import User
from models.SpotifyAuthDetails import SpotifyAuthDetails

from repositories.exceptions import AuthenticationFailureException, SpotifyAuthenticationFailureException, UserNotFoundException
from repositories.user import UserRepository
from repositories.stats import StatsRepository

import requests
import base64

from jose import jwt as joseJWT
from jose import JWTError as joseJWTError

class AuthFlowRepository:
    @staticmethod
    def create_JWT(user:User) -> JWToken:
        logger.debug(f"Creating JWT for {user.id=}")
        to_encode = {'id':str(user.id),'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)}
        encoded_jwt = joseJWT.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return JWToken(access_token=encoded_jwt,token_type="bearer")

    @staticmethod
    def validate_JWT(jwt_str:str) -> str:
        try:
            payload = joseJWT.decode(str(jwt_str), JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            id: str = payload.get("id")
            if id is None:
                raise AuthenticationFailureException()
        except joseJWTError:
            raise AuthenticationFailureException()
        return id

    @staticmethod
    def auth_required_wrapper(handler):
        # Add jwt to the handler, otherwise just check the jwt
        if "jwt" not in inspect.signature(handler).parameters:
            def wrapper(*args,jwt: str = Header(None), **kwargs):
                if str(jwt) == str(Header(None)):
                    raise AuthenticationFailureException()
                AuthFlowRepository.validate_JWT(jwt)
                return handler(*args, **kwargs)
        else:
            def wrapper(*args,**kwargs):
                if kwargs['jwt'] is None:
                    raise AuthenticationFailureException()
                AuthFlowRepository.validate_JWT(kwargs['jwt'])
                return handler(*args,**kwargs)

        # Fix signature of wrapper
        wrapper.__signature__ = inspect.Signature(
            parameters = [
                # Use all parameters from handler
                *inspect.signature(handler).parameters.values(),
                # Skip *args and **kwargs from wrapper parameters:
                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(wrapper).parameters.values()
                )
            ],
            return_annotation = inspect.signature(handler).return_annotation,
        )
        wrapper.__name__ = handler.__name__
        return wrapper

    @staticmethod
    def auth_required_dep(jwt: str = Header(None)) -> PydanticObjectId:
        if str(jwt) == str(Header(None)):
            raise AuthenticationFailureException()
        id: str =  AuthFlowRepository.validate_JWT(jwt)
        return PydanticObjectId(id)



    @staticmethod
    def login() -> RedirectResponse:
        scopes: str = SPOTIFY_SCOPE 
        response: RedirectResponse = RedirectResponse(
            f"https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={scopes}&redirect_uri={SPOTIFY_REDIRECT_URI}"
        )
        return response

    @staticmethod
    def login_callback(code: str) -> RedirectResponse:
        # Minimal testing coverage as this is a pretty integrated system with spotify. Would include a lot of faff to test. cba for now
        str_token = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        basic_token_bytes = base64.urlsafe_b64encode(str_token.encode("utf-8"))
        basic_token_str = str(basic_token_bytes, "utf-8")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Authorization": f"Basic {basic_token_str}"
        }

        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI
        }

        res: HTTPResponse = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=body
        )
        if res.ok:  
            res = res.json()
            res['expires_at'] = timedelta( seconds= res['expires_in']) + utils.get_time()
            spotifyAuthDetails = SpotifyAuthDetails(**res)

            res: HTTPResponse = requests.get("https://api.spotify.com/v1/me", headers={
                "Authorization": f"Bearer {spotifyAuthDetails.access_token}"
            })

            if res.ok:
                res = res.json()
                user = User(
                    spotifyAuthDetails=spotifyAuthDetails,
                    user_id=res['id'])

                try:
                    user: User = UserRepository.get_by_user_id(user_id=user.user_id)
                    logger.debug(f"User with id {user.id} was found")
                except UserNotFoundException:
                    user.id = PydanticObjectId()
                    user: User = UserRepository.create(user)
                    logger.debug(f"User with id {user.id} was created")
                    StatsRepository.user_creation()

                jwt = AuthFlowRepository.create_JWT(user)
                rr = RedirectResponse("/")
                rr.set_cookie(key="jwt", value=jwt.access_token)
                return rr
            else:
                raise SpotifyAuthenticationFailureException()

        else:
            logger.error("Unable to authenticate.", res.text)
            raise SpotifyAuthenticationFailureException()
