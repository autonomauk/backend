from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from config import settings

client: MongoClient = MongoClient(settings.database.URI)
db: Database = client[settings.database.DB]

users_collection: Collection = db["users"]

stats_collection: Collection = db['stats']