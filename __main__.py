import argparse
import os
import uvicorn
from loguru import logger
import sys

parser = argparse.ArgumentParser(prog='SpotifyPlaylister', description='SpotifyPlaylister CLI')
parser.add_argument('--worker', action='store_true')
parser.add_argument('--server', action='store_true')

parser.add_argument("--env", choices=['production','development'], default='development')

if __name__ == "__main__":
    args = parser.parse_args()

    os.environ['SP_ENV'] = args.env


    logger.configure(**{
        "handlers": [
            {
                "sink": sys.stderr, 
                "format": "UP {elapsed} | <level>{level: <8}</level> | PID {process} | <cyan>{file}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level":"INFO" if args.env=="production" else "DEBUG"
                }
        ]})

    if args.server:
        from config import PORT, UVICORN_ROOT_PATH
        uvicorn.run("api:app", host="127.0.0.1", port=PORT, root_path=UVICORN_ROOT_PATH, reload=args.env=="development")
    elif args.worker:
        from workers.SpotiCron import SpotiCron
        SpotiCron()
    else:
        parser.print_help()
