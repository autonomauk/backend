from starlette.responses import JSONResponse
from repositories.exceptions import BaseAPIException
from  models.errors import BaseError
import pytest
from fastapi import status as statuscode
import json

@pytest.fixture
def base_api_exception():
    yield BaseAPIException()

class TestBaseAPIException:
    def test_vars(self, base_api_exception):
        exception: BaseAPIException = base_api_exception
        assert exception.message == "Generic error"
        assert exception.code == statuscode.HTTP_500_INTERNAL_SERVER_ERROR
        assert exception.model == BaseError

    def test_response_model(self):
        exception: BaseAPIException = BaseAPIException.response_model()
        assert exception[BaseAPIException.code] == {"model":BaseAPIException.model}

    def test_response(self, base_api_exception):
        exception: BaseAPIException = base_api_exception
        response: JSONResponse = exception.response()
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == BaseAPIException.code
        assert json.loads(response.body) == {"message":exception.message}

    def test___str__(self, base_api_exception):
        exception: BaseAPIException = base_api_exception

        assert str(exception) == exception.message