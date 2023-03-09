import pytest

from config import settings
from models.ObjectId import PydanticObjectId
from models.SpotifyAuthDetails import SpotifyAuthDetails
from models.User import User
from repositories.exceptions import UserNotFoundException
from repositories.user import UserRepository
from utils import get_non_tzaware_time
from workers.SpotiCron.main import SpotiCronRunnerPerUser


@pytest.fixture
def now():
    return get_non_tzaware_time()


@pytest.fixture(scope="session")
def playlist_name():
    return str(PydanticObjectId())


@pytest.fixture(scope="session")
def spotify_auth():
    auth = SpotifyAuthDetails(**settings.spotify.test_user.auth)
    auth.expires_at = auth.expires_at.replace(tzinfo=None)
    yield auth

@pytest.fixture(scope="session")
def user_id():
    return settings.spotify.test_user.name


@pytest.fixture(scope="session")
def user(playlist_name, user_id, spotify_auth):
    try:
        user = UserRepository.get_by_user_id(user_id)
    except UserNotFoundException:
        user = UserRepository.create(User(spotifyAuthDetails=spotify_auth, user_id=user_id))
    yield user
    UserRepository.delete(user.id)


@pytest.fixture(scope="session")
def spoticron_runner(user, playlist_name):
    yield SpotiCronRunnerPerUser(user=user, playlist_name=playlist_name)
