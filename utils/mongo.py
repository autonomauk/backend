from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from config import *

client: MongoClient = MongoClient(MONGODB_URI)
db: Database = client[MONGODB_DB]

users_collection: Collection = db["users"]

stats_collection: Collection = db['stats']