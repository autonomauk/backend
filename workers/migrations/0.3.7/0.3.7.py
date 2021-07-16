"""
Merges _id and id to use the bson.ObjectId rather than UUIDv4
"""

from pymongo.database import Database
import uuid

name = "0.3.7"
dependencies = []


def upgrade(db: Database):
    db.users.update_many({'id':{"$exists": True}},{'$unset':{'id': ''}})

def downgrade(db: Database):
    for user in db.users.find({'id':{"$exists": False}}):
        db.users.find_one_and_update({'_id':user['_id']},{'$set':{'id':str(uuid.uuid4())}})