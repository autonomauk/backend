from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from config import settings

client: MongoClient = MongoClient(settings.db.MONGODB_URI)
db: Database = client[settings.db.MONGODB_DB]

users_collection: Collection = db["users"]

stats_collection: Collection = db['stats']