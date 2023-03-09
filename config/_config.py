"""
Module to house the core setup of the dynaconf settings

"""
from itertools import count

from dynaconf import Dynaconf
from loguru import logger
import os

_c = count()
def get_setting():
    logger.debug(f"Running get_settings (count = {next(_c)}) with {os.environ['ENV_FOR_DYNACONF']=}")
    return Dynaconf(
        envvar_prefix="AUTONOMA",
        settings_files=["settings.toml", ".secrets.toml"],
        # Allows [default], [development], etc.
        # https://www.dynaconf.com/configuration/#environments
        environments=True,
        apply_default_on_none=True,
    )


settings = get_setting()
