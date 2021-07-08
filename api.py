from repositories.stats import StatsRepository
from models.Settings import Settings
from repositories.user import UserRepository
from fastapi.param_functions import Header
from repositories.auth_flow import AuthFlowRepository
from repositories.exceptions import AuthenticationFailureException, BaseAPIException, UserNotFoundException
from models.ObjectId import PydanticObjectId

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from starlette.responses import RedirectResponse

import config

app = FastAPI(
    title="AutonomaAPI",
    docs_url=None if config.ENV == "production" else '/docs',
    redoc_url=None if config.ENV == "production" else '/redoc',
    openapi_url=None if config.ENV == "production" else '/openapi.json'
)

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) # TODO Change this


@app.exception_handler(BaseAPIException)
def http_exception_handler(request, exc) -> BaseAPIException:
    return exc.response()

#####################
# LOGIN/LOGOUT FLOW #
#####################


@app.get("/login",
         description="Begin login flow via Spotify")
def user_login() -> RedirectResponse:
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
