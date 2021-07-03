import pymongo
from utils.mongo import *

class TestMongo:
    def test_types(self):
        assert isinstance(client, pymongo.MongoClient)
        assert isinstance(db, pymongo.database.Database)
        assert isinstance(users_collection, pymongo.collection.Collection)
        assert isinstance(stats_collection, pymongo.collection.Collection)

    def test_connection(self):
        client.server_info()

    def test_collections_are_correct(self):
        assert users_collection.name is "users"
        assert stats_collection.name is "stats"