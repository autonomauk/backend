from os import stat
from typing import Type
from fastapi import status as statuscode
from fastapi.responses import JSONResponse

from models.errors import *

class BaseAPIException(Exception):
    message = "Generic error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message",self.message)
        self.message = kwargs['message']
        self.data = self.model(**kwargs)
    
    def __str__(self) -> str:
        return self.message

    def response(self) -> JSONResponse:
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code:{"model":cls.model}}

class BaseIdentifiedExcpetion(BaseAPIException):
    message = "Entity error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier,**kwargs)

class NotFoundException(BaseIdentifiedExcpetion):
    message = "The entity does not exist"
    code = statuscode.HTTP_404_NOT_FOUND
    model = NotFoundError

class AlreadyExistsException(BaseIdentifiedExcpetion):
    message = "The entity already exists"
    code = statuscode.HTTP_409_CONFLICT
    model = AlreadyExistsError

class UserNotFoundException(NotFoundException):
    message = "The user does not exist"

class UserAlreadyExistsExcpetion(AlreadyExistsException):
    message = "The user already exists"

class AuthenticationFailureException(BaseAPIException):
    message = "Failure to authenticate"
    code = statuscode.HTTP_403_FORBIDDEN
    model = AuthenticationFailure

class SpotifyAuthenticationFailureException(AuthenticationFailureException):
    message = "Failure to authenticate with Spotify"

def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
