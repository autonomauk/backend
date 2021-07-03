from repositories.stats import StatsRepository
from models.Settings import Settings
from models.User import User
import loguru
from repositories.user import UserRepository
from fastapi.param_functions import Depends, Header
from repositories.auth_flow import AuthFlowRepository
from models.JWToken import JWToken
from repositories.exceptions import AuthenticationFailureException, BaseAPIException, UserNotFoundException
from models.SpotifyAuthDetails import SpotifyAuthDetailsFields
from models.ObjectId import PydanticObjectId

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from loguru import logger

from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from config import *

import crontab

app = FastAPI(
    title="SpotifyPlaylister",
    docs_url=None if config.SP_ENV == "production" else '/docs',
    redoc_url=None if config.SP_ENV == "production" else '/redoc',
    openapi_url=None if config.SP_ENV == "production" else '/openapi.json'
)

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])  # TODO Change this


@app.exception_handler(BaseAPIException)
def http_exception_handler(request, exc) -> BaseAPIException:
    return exc.response()

#####################
# LOGIN/LOGOUT FLOW #
#####################


@app.get("/login",
         description="Begin login flow via Spotify")
def _user_login() -> RedirectResponse:
    return AuthFlowRepository.login()


@app.get("/login/callback",
         description="Handles Spotify callback after successful login"
         )
def user_login_callback(code: str) -> RedirectResponse:
    return AuthFlowRepository.login_callback(code)


########
# USER #
########

### Me ####

@app.delete('/me',
            responses={
                **AuthenticationFailureException.response_model(),
                **UserNotFoundException.response_model()}
            )
@AuthFlowRepository.auth_required
def delete_user(jwt: str = Header(None)) -> str:
    id = AuthFlowRepository.validate_JWT(jwt)
    UserRepository.delete(PydanticObjectId.validate(id))
    logger.info(f'User with {id=} was deleted')
    StatsRepository.user_deletion()
    return "OK"

### Settings ###


@app.get("/me/settings",
         response_model=Settings,
         responses={
             **AuthenticationFailureException.response_model(),
             **UserNotFoundException.response_model()}
         )
@AuthFlowRepository.auth_required
def read_users_settings(jwt: str = Header(None)):
    id = AuthFlowRepository.validate_JWT(jwt)
    user = UserRepository.get(id)
    return user.settings


@app.patch("/me/settings",
           response_model=Settings,
           responses={
               **AuthenticationFailureException.response_model(),
               **UserNotFoundException.response_model()}
           )
@AuthFlowRepository.auth_required
def update_users_settings():
    pass

########
# Home #
########

@app.get("/")
def root():
    return RedirectResponse("/")
