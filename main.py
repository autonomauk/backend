from repositories.exceptions import AuthenticationFailureException
from models.SpotifyAuthDetails import SpotifyAuthDetailsFields

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from starlette.responses import RedirectResponse

from config import *

import crontab

app = FastAPI(
    title="SpotifyPlaylister"
)

#####################
# LOGIN/LOGOUT FLOW #
#####################

from repositories.auth_flow import AuthFlowRepository

@app.get("/login",
         description="Begin login flow via Spotify")
def _user_login() -> RedirectResponse:
    return AuthFlowRepository.login()

@app.get("/login/callback",
         description="Handles Spotify callback after successful login"
         )
def user_login_callback(code: str) -> RedirectResponse:
    return AuthFlowRepository.login_callback(code)


#################
# USER SETTINGS #
#################

@app.get("/settings/me",
    responses={**AuthenticationFailureException.response_model()}
    )
@AuthFlowRepository.auth_required
def read_users_settings():
    pass

@app.patch("/settings/me",
    responses={**AuthenticationFailureException.response_model()}
)
@AuthFlowRepository.auth_required
def update_users_settings():
    pass

########
# Home #
########

# @app.get("/")
# def root():
#     return RedirectResponse("/docs")
