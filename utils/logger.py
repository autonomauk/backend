import functools
from loguru import logger
import sys
import time


def get_logger_config(verbosity: int = 0): # pragma: no cover

    if verbosity == 0:
        LOG_LEVEL = "INFO"
    elif verbosity == 1:
        LOG_LEVEL = "DEBUG"
    elif verbosity == 2:
        LOG_LEVEL = "TRACE"
    else:
        raise ValueError(f"Invalid value {verbosity=}")

    return {
        "handlers": [
            {
                "sink": sys.stderr,
                "format": "UP {elapsed} | <level>{level: <8}</level> | USER {extra[user_id]} | <cyan>{file}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": LOG_LEVEL,
                "filter": lambda record: record["extra"]["user_id"] != "NONE"
            },
            {
                "sink": sys.stderr,
                "format": "UP {elapsed} | <level>{level: <8}</level> | <cyan>{file}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": LOG_LEVEL,
                "filter": lambda record: record["extra"]["user_id"] == "NONE"
            }
        ],
        "extra": {"user_id": "NONE"}}


def timeit(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        logger_ = logger
        if len(args) > 0 and "log" in dir(args[0]):
            logger_ = args[0].log
        logger_.log("DEBUG", "Function '{}' executed in {:.3f} s",
                    func.__name__, end - start)

        return result
    return wrapped
