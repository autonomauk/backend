import utils
from models.errors import AuthenticationFailure
from models.JWToken import JWToken
from typing import Optional
from fastapi import Header
from datetime import timedelta,datetime
from models.User import User
from models.SpotifyAuthDetails import SpotifyAuthDetails
from repositories.exceptions import AuthenticationFailureException, SpotifyAuthenticationFailureException, UserNotFoundException
from repositories.user import UserRepository
from starlette.responses import RedirectResponse
import inspect
from config import *

import requests
import base64

from jose import jwt as joseJWT
from jose import JWTError as joseJWTError



from loguru import logger

class AuthFlowRepository:
    @staticmethod
    def create_JWT(user:User) -> JWToken:
        to_encode = {'id':user.id,'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)}
        encoded_jwt = joseJWT.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return JWToken(access_token=encoded_jwt,token_type="bearer")

    @staticmethod
    def validate_JWT(jwt_str:str) -> str:
        try:
            payload = joseJWT.decode(jwt_str, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            id: str = payload.get("id")
            if id is None:
                raise AuthenticationFailureException()
        except joseJWTError:
            raise AuthenticationFailureException()
        return id

    @staticmethod
    def auth_required(handler):
        # Add jwt to the handler, otherwise just check the jwt
        if "jwt" not in inspect.signature(handler).parameters:
            def wrapper(*args,jwt: str = Header(None), **kwargs):
                if jwt is None:
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
    def login() -> RedirectResponse:
        scopes: str = SPOTIFY_SCOPE 
        response: RedirectResponse = RedirectResponse(
            f"https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={scopes}&redirect_uri={SPOTIFY_REDIRECT_URI}"
        )
        return response

    @staticmethod
    def login_callback(code: str) -> RedirectResponse:
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

        res = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=body
        )

        if res.ok:
            res = res.json()
            res['expires_at'] = res['expires_in'] + utils.get_time()
            spotifyAuthDetails = SpotifyAuthDetails(**res)


            res = requests.get("https://api.spotify.com/v1/me", headers={
                "Authorization": f"Bearer {spotifyAuthDetails.access_token}"
            })

            user = User(
                spotifyAuthDetails=spotifyAuthDetails,
                user_id=res.json()['id'])

            try:
                user: User = UserRepository.get_by_user_id(user_id=user.user_id)
                logger.debug(f"User with id {user.id} was found")
            except UserNotFoundException:
                user: User = UserRepository.create(user)
                logger.debug(f"User with id {user.id} was created")

            jwt = AuthFlowRepository.create_JWT(user)
            rr = RedirectResponse(f"/")
            rr.set_cookie(key="jwt", value=jwt.access_token)
            return rr

        else:
            logger.error("Unable to authenticate.", res.text)
            raise SpotifyAuthenticationFailureException()
