from pymongo_migrate.mongo_migrate import MongoMigrate # pragma: no cover
from pymongo_migrate.cli import get_logger             # pragma: no cover
import os                                              # pragma: no cover
from utils.mongo import client as pymongo_client       # pragma: no cover

def run_migrations(): # pragma: no cover
    mm = MongoMigrate(pymongo_client, migrations_dir=os.path.join(os.getcwd(),'workers','migrations'))
    mm.logger = get_logger(verbose=1)
    mm.upgrade()