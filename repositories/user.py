from pymongo import collection, cursor
from repositories.exceptions import UserNotFoundException
from utils import users_collection,get_time,get_uuid
from models.User import User, Users

class UserRepository:
    @staticmethod
    def get(id: str) -> User:
        document = users_collection.find_one({'id':id})
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

        document = create.dict()
        document['createdAt'] = document['updatedAt'] = get_time()
        document['id'] = get_uuid()

        results = users_collection.insert_one(document)
        assert results.acknowledged

        return UserRepository.get(document['id'])

    @staticmethod
    def update(id, update: User):
        document = update.dict()
        document["updatedAt"] = get_time()

        results = users_collection.update_one({'id':id}, {"$set":document})
        if not results.modified_count:
            raise UserNotFoundException(identifier=id)

    @staticmethod
    def delete(id: str):
        result = users_collection.delete_one({'id':id})
        if not result.deleted_count:
            raise UserNotFoundException(identifier=id)