
"""
Add enabled to user
"""

from pymongo.database import Database

name = "0.6.1"
dependencies = []

def upgrade(db: Database):
    db.users.update_many({},{'$set':{'settings.enabled': True}})

def downgrade(db: Database):
    for user in db.users.find({'settings.enabled':{"$exists": True}}):
        db.users.find_one_and_update({'_id':user['_id']},{'$unset':'settings.enabled'})
