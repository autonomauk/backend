"""
Module to house the core setup of the dynaconf settings

"""
from dynaconf import Dynaconf

settings: Dynaconf = Dynaconf(
    envvar_prefix="AUTONOMA",
    settings_files=["settings.toml", ".secrets.toml"],
    # Allows [default], [development], etc.
    # https://www.dynaconf.com/configuration/#environments
    environments=True,
    apply_default_on_none=True
)
