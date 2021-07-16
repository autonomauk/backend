
"""
Adds track_log to user
"""

from pymongo.database import Database

name = "0.6.0"
dependencies = []

def upgrade(db: Database):
    db.users.update_many({},{'$set':{'track_log': []}})

def downgrade(db: Database):
    for user in db.users.find({'track_log':{"$exists": True}}):
        db.users.find_one_and_update({'_id':user['_id']},{'$unset':'track_log'})
