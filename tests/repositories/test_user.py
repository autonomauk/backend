import copy
from models.music.Track import Track, Tracks
from time import sleep

import pytest

from models.ObjectId import PydanticObjectId
from models.User import User, Users
from repositories.exceptions import UserNotFoundException
from repositories.user import UserRepository
from utils import users_collection

from tests.variables import USER_DICT, TRACK_DICT_1, TRACK_DICT_2

# pylint was complaingin about func(user) being overwritten in functions as an arg.
# However, this is exactly how pytest uses fixtures. Hence we disable it here.

# pylint:disable=redefined-outer-name

@pytest.fixture()
def user():
    # Startup code
    user = User(**USER_DICT())
    id: PydanticObjectId = copy.deepcopy(user.id)
    yield user
    # Cleanup code
    try:
        UserRepository.delete(id)
    except UserNotFoundException:
        pass

class TestUserRepository:
    def test_type_checking(self, user: User):
        for func in [UserRepository.get,
                     UserRepository.delete,
                     lambda x: UserRepository.update(x, user),
                     lambda x: UserRepository.update(PydanticObjectId(), x),
                     UserRepository.create,
                     UserRepository.get_by_user_id,
                     lambda x: UserRepository.add_tracks_to_log(PydanticObjectId(), x),
                     lambda x: UserRepository.add_tracks_to_log(x, []),
                     UserRepository.read_track_log
                     ]:

            with pytest.raises(ValueError):
                func(100)

    def test_create(self, user: User):
        test_req_before_creation = users_collection.find_one({'_id': user.id})
        assert test_req_before_creation is None

        UserRepository.create(user)

        test_req_after_creation = users_collection.find_one({'_id': user.id})
        assert test_req_after_creation is not None
        assert user.dict() == test_req_after_creation

    def test_get(self, user: User):
        UserRepository.create(user)  # Assume this works because of testing

        # Get the user
        got_user: User = UserRepository.get(user.id)

        # Are they the same?
        assert got_user.dict() == user.dict()

        # Edit the entry to check this test isn't flawed
        users_collection.find_one_and_update(
            {'_id': user.id}, {"$set": {"user_id": "thisisnotwhatyouwereexpecting"}})

        # Get user again
        got_user: User = UserRepository.get(user.id)

        # Check they're different
        assert got_user.dict() != user.dict()

        # but not too different...
        got_user_dict = got_user.dict()
        user_dict = user.dict()
        got_user_dict.pop('user_id')
        user_dict.pop('user_id')

        assert got_user_dict == user_dict

        with pytest.raises(UserNotFoundException):
            id = PydanticObjectId()
            UserRepository.get(id)

    def test_update(self, user: User):
        UserRepository.create(user)  # Assume this works because of testing

        # Update user
        # otherwise edited_user is just a reference to user
        edited_user: User = copy.deepcopy(user)
        edited_user.user_id = "updated_uid"
        edited_user_dict: dict = edited_user.dict()
        sleep(0.5)
        UserRepository.update(user.id, edited_user)

        got_edited_user: User = UserRepository.get(edited_user.id)
        got_edited_user_dict: dict = got_edited_user.dict()

        got_edited_user_dict.pop('updatedAt')
        edited_user_dict.pop('updatedAt')
        assert got_edited_user_dict == edited_user_dict
        assert edited_user.updatedAt < got_edited_user.updatedAt
        assert edited_user.user_id != user.user_id

        with pytest.raises(UserNotFoundException):
            UserRepository.update(PydanticObjectId(), user)

    def test_get_user_by_id(self, user: User):
        # Change name to avoid conflicts with other tests
        user.user_id = "unique-ish name"
        # Create the user
        UserRepository.create(user)

        # Get user. Note, it gets the first user by id so if there are multiple this will not work
        got_user = UserRepository.get_by_user_id(user.user_id)

        assert got_user.dict() == user.dict()

        # Check for non-existent users
        with pytest.raises(UserNotFoundException):
            UserRepository.get_by_user_id("thisdoesntexist")

        # Delete the custom user
        UserRepository.delete(user.id)

    def test_delete(self, user: User):
        UserRepository.create(user)

        assert UserRepository.get(user.id) is not None  # User exists

        # Delete user
        UserRepository.delete(user.id)

        # Try to get user
        with pytest.raises(UserNotFoundException):
            UserRepository.get(user.id)

        # Ensure delete raises error if no user found
        with pytest.raises(UserNotFoundException):
            UserRepository.delete(user.id)

    def test_list(self, user: User):
        users_collection.drop()

        user1: User = copy.deepcopy(user)
        user2: User = copy.deepcopy(user)
        user2.id = PydanticObjectId()

        UserRepository.create(user1)
        UserRepository.create(user2)

        users: Users = UserRepository.list()

        # Create 2 sets holding ALL user id's. Find difference and if that is 
        # False (i.e. empty) then we have found all users
        assert not set([u.id for u in users]) - set([user1.id, user2.id])
        assert len(users) == 2
        assert all((isinstance(f, User) for f in users))

    def test_add_tracks_to_log(self, user: User):
        UserRepository.create(user)

        tracks = Tracks([Track(**TRACK_DICT_1), Track(**TRACK_DICT_2)])

        UserRepository.add_tracks_to_log(user.id, tracks)

        read_user: User = UserRepository.get(user.id)
        
        for f,g in zip(tracks, read_user.track_log):
            # mongoDB rounds dt to ms
            delattr(f,'createdAt')
            delattr(f,'updatedAt')
            delattr(g,'createdAt')
            delattr(g,'updatedAt')
            assert f == g 