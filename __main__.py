import argparse
import uvicorn
from loguru import logger
import os
parser = argparse.ArgumentParser(prog='Autonoma', description='Autonoma CLI')

parser.add_argument('--worker', action='store_true')
parser.add_argument('--server', action='store_true')
parser.add_argument('--migrate', action='store_true')
parser.add_argument('--profile', action='store_true')
parser.add_argument('--one-shot', action='store_true', dest="oneshot")
parser.add_argument('-T', '--threaded', action='store_true', dest="threaded")
parser.add_argument("--env", choices=['production','development'], default='development')
parser.add_argument("-v","--verbose", action='count', default=1, help="increase output verbosity")

if __name__ == "__main__":
    args = parser.parse_args()

    os.environ['ENV_FOR_DYNACONF'] = args.env
    from config import settings

    from utils.logger import get_logger_config
    logger.configure(**get_logger_config(args.verbose))

    if args.profile and (args.server or args.migrate):
        logger.warning("Profiling is not supported for server yet. Try re-running with --worker")
    
    if args.oneshot and (args.server or args.migrate):
        logger.warning("One-shot is not supported for server yet. Try re-running with --worker")
    
    if args.threaded and (args.server or args.migrate):
        logger.warning("Threading is not supported for server yet. Try re-running with --worker")

    with settings.using_env(args.env):
        if args.server:
            uvicorn.run("api:app", host=settings.server.IP, port=int(settings.server.PORT), reload=args.env=="development")
        elif args.worker:
            from workers.SpotiCron import SpotiCron
            SpotiCron(profile=args.profile, oneshot=args.oneshot, threaded=args.threaded, dev=args.env=="development")
        elif args.migrate:
            from workers.MongoMigrate import run_migrations
            run_migrations()
        else:
            parser.print_help()
