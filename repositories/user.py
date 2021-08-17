from models.music.TrackLog import TrackLog, TrackLogs
from typing import List
from bson.objectid import ObjectId

from utils import users_collection, get_time
from models.music import Track, Tracks
from models.User import User, Users
from models.ObjectId import PydanticObjectId
from repositories.exceptions import UserNotFoundException


class UserRepository:
    @staticmethod
    def get(id: PydanticObjectId) -> User:
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        document = users_collection.find_one({'_id': id})
        if not document:
            raise UserNotFoundException(identifier=id)
        return User(**document)

    @staticmethod
    def get_by_user_id(user_id: str):
        if not isinstance(user_id, str):
            raise ValueError(f"user_id is type {type(user_id)} and not str")

        document = users_collection.find_one({'user_id': user_id})
        if not document:
            raise UserNotFoundException(identifier=user_id)
        return User(**document)

    @staticmethod
    def list(filter: dict={}) -> Users:
        cursor = users_collection.find(filter)
        return [User(**document) for document in cursor]

    @staticmethod
    def create(create: User) -> User:
        if not isinstance(create, User):
            raise ValueError(f"create is type {type(create)} and not User")

        document = create.dict()
        results = users_collection.insert_one(document)
        assert results.acknowledged
        return create

    @staticmethod
    def update(id: PydanticObjectId, update: User):
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")
        if not isinstance(update, User):
            raise ValueError(f"id is type {type(id)} and not User")

        document = update.dict()
        document['updatedAt'] = get_time()
        results = users_collection.update_one({'_id': id}, {"$set": document})
        if not results.modified_count:
            raise UserNotFoundException(identifier=id)

    @staticmethod
    def delete(id: PydanticObjectId):
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        result = users_collection.delete_one({'_id': id})
        if not result.deleted_count:
            raise UserNotFoundException(identifier=id)

    @staticmethod
    def add_tracks_to_log(id: PydanticObjectId, track_logs: TrackLogs):
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        if isinstance(track_logs, (set,list, tuple)):
            for f in track_logs:
                if not isinstance(f, TrackLog):
                    raise ValueError(f"track is type {type(f)} and not {type(TrackLog)}")
        else:
            raise ValueError(f"type {type(track_logs)} is not iterable")


        document: List[dict] = [f.dict() for f in track_logs]
        results = users_collection.update_one(
            {'_id': id}, {'$push': {'track_log': {'$each': document}}})
        if not results.modified_count:
            raise UserNotFoundException(identifier=id)

    @staticmethod
    def read_track_log(id: PydanticObjectId, offset: int, length: int) -> TrackLogs:
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        aggregation: List[dict] =[
            {
                '$match': {
                    '_id': id
                }
            }, {
                '$project': {
                    'track_log': 1, 
                    '_id': 0
                }
            }, {
                '$unwind': {
                    'path': '$track_log', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$sort': {
                    'track_log.createdAt': -1
                }
            }]

        if offset>0:
            aggregation.append({'$skip': offset})

        aggregation.append({'$limit': length})

        cursor = users_collection.aggregate(aggregation)

        if not cursor:
            raise UserNotFoundException(identifier=id)

        total_cursor = users_collection.aggregate([{"$match":{'_id': id}},{"$project":{"count": {"$size":"$track_log"}}}])

        total: int = [f.get('count') for f in total_cursor][0]
        result: TrackLogs = [TrackLog(**f['track_log']) for f in cursor if f != {}] # Aggregation pipeline will return {} if there is nothing

        return result, total
