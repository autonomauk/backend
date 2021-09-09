from tests.variables import USER_DICT
from models.User import User
import pytest

@pytest.fixture()
def user():
    yield User(**USER_DICT())


class TestUser:
    def test_dict_func(self, user: User):
        user_dict: dict = user.dict()
        user_dict_keys: list = user_dict.keys()

        assert "id" not in user_dict_keys

        user_dict: dict = USER_DICT()
        user_dict.pop('_id')
        for f in user_dict.keys():
            assert f in user_dict_keys