import copy
from datetime import datetime, timedelta
from routers.me.track_log.track_log import track_log
from models.music.Playlist import Playlist
from models.music.TrackLog import TrackLog, TrackLogs
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
                     lambda x: UserRepository.read_track_log(x,0,10),
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
        user1: User = copy.deepcopy(user)
        user2: User = copy.deepcopy(user)
        user2.id = PydanticObjectId()
        user2.settings.enabled = False

        UserRepository.create(user1)
        UserRepository.create(user2)

        users: Users = UserRepository.list()
        # Create 2 sets holding ALL user id's. Find difference and if that is 
        # set() then we have found all users that we added. Other tests may be running
        # and therefore we assume that if we have our 2 users the test was successful.
        assert set([user1.id, user2.id]) - set([u.id for u in users]) == set()
        assert all((isinstance(f, User) for f in users))
        
        users: Users = UserRepository.list({"settings.enabled": True})
        assert user1.id in (u.id for u in users)
        assert all((isinstance(f, User) for f in users))

    def test_add_tracks_to_log(self, user: User):
        UserRepository.create(user)

        tracks = [TrackLog(track=f,playlist=Playlist(name="test")) for f in [Track(**TRACK_DICT_1), Track(**TRACK_DICT_2)]]

        UserRepository.add_tracks_to_log(user.id, tracks)

        read_user: User = UserRepository.get(user.id)

        track_log = read_user.track_log 

        for i in range(len(track_log)):
            # mongoDB rounds dt to ms
            delattr(track_log[i],'createdAt')
            delattr(track_log[i],'updatedAt')
        for i in range(len(tracks)):
            # mongoDB rounds dt to ms
            delattr(tracks[i],'createdAt')
            delattr(tracks[i],'updatedAt')

        assert set([str(f) for f in tracks]) - set([str(f) for f in track_log]) == set()

        # Sanity check
        tracks.append("hi")
        assert set([str(f) for f in tracks]) - set([str(f) for f in track_log]) == set(['hi'])

    def test_read_track_log(self, user: User):
        UserRepository.create(user)

        tracks, total = UserRepository.read_track_log(user.id, 0, 10)
        assert len(tracks) == 10
        # Check if sorted properly
        for i in range(len(tracks)-1):
            assert tracks[i].createdAt - tracks[i+1].createdAt >= timedelta(seconds=0)
        assert total == len(user.track_log)
        assert set((str(f) for f in tracks)) - set((str(f) for f in user.track_log)) == set()
        
        tracks, total = UserRepository.read_track_log(user.id, 0, float('inf'))
        assert len(tracks) == len(user.track_log)
        assert total == len(user.track_log)
        assert set((str(f) for f in tracks)) - set((str(f) for f in user.track_log)) == set()

        offset = 0
        length = 1
        track_log = []
        while True:
            tracks, total = UserRepository.read_track_log(user.id, offset, length)
            track_log += tracks
            if len(track_log) == total:
                break
            else:
                offset += length

        assert set((str(f) for f in track_log)) - set((str(f) for f in user.track_log)) == set()

        # Sanity check
        track_log.append('hi')
        assert set((str(f) for f in track_log)) - set((str(f) for f in user.track_log)) == set(['hi'])
