from bson.objectid import ObjectId
from loguru import logger
from pymongo import collection, cursor
from repositories.exceptions import UserNotFoundException
from utils import users_collection,get_time,get_uuid
from models.User import User, Users
from models.ObjectId import PydanticObjectId

class UserRepository:
    @staticmethod
    def get(id: PydanticObjectId) -> User:
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        document = users_collection.find_one({'_id':id})
        if not document:
            raise UserNotFoundException(identifier=id)
        return User(**document)

    @staticmethod
    def get_by_user_id(user_id:str):
        document = users_collection.find_one({'user_id':user_id})
        if not document:
            raise UserNotFoundException(identifier=user_id)
        return User(**document)

    @staticmethod
    def list() -> Users:
        cursor = users_collection.find()
        return [User(**document) for document in cursor]

    @staticmethod
    def create(create: User) -> User:
        if not isinstance(create, User):
            raise ValueError(f"create is type {type(create)} and not User")

        document = create.dict()
        results = users_collection.insert_one(document)
        assert results.acknowledged

        return UserRepository.get(document['_id'])

    @staticmethod
    def update(id: PydanticObjectId, update: User):
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")
        
        update.updatedAt = get_time()
        document = update.dict()
        results = users_collection.update_one({'_id':id}, {"$set":document})
        if not results.modified_count:
            raise UserNotFoundException(identifier=id)

    @staticmethod
    def delete(id: PydanticObjectId):
        if not isinstance(id, ObjectId):
            raise ValueError(f"id is type {type(id)} and not ObjectId")

        result = users_collection.delete_one({'_id':PydanticObjectId(id)})
        if not result.deleted_count:
            raise UserNotFoundException(identifier=id)