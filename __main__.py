import argparse
import os

parser = argparse.ArgumentParser(prog='SpotifyPlaylister', description='SpotifyPlaylister CLI')
parser.add_argument('--worker', action='store_true')
parser.add_argument('--server', action='store_true')

parser.add_argument("--env", choices=['production','development'], default='development')

if __name__ == "__main__":
    args = parser.parse_args()

    os.environ['SP_ENV'] = args.env

    if args.server:
        import uvicorn
        from config import PORT
        uvicorn.run("api:app", host="127.0.0.1", port=PORT, root_path='/api')
        
    elif args.worker:
        from workers.SpotiCron import SpotiCron
        SpotiCron()

    else:
        parser.print_help()