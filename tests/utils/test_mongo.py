import pymongo
from utils.mongo import client, db, users_collection, stats_collection

class TestMongo:
    def test_types(self):
        assert isinstance(client, pymongo.MongoClient)
        assert isinstance(db, pymongo.database.Database)
        assert isinstance(users_collection, pymongo.collection.Collection)
        assert isinstance(stats_collection, pymongo.collection.Collection)

    def test_connection(self):
        client.server_info()

    def test_collections_are_correct(self):
        assert users_collection.name == "users"
        assert stats_collection.name == "stats"