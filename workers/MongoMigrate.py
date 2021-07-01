from pymongo_migrate.mongo_migrate import MongoMigrate
from pymongo_migrate.cli import get_logger
import os
from utils.mongo import client as pymongo_client

def run_migrations():
    mm = MongoMigrate(pymongo_client, migrations_dir=os.path.join(os.getcwd(),'workers','migrations'))
    mm.logger = get_logger(verbose=1)
    mm.upgrade()