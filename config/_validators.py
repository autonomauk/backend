"""
Module to house dynaconf validators

.. note::

    `dynaconf` is going to use :class:`pydantic.BaseSettings` as of v4

"""
from typing import Any
from typing import Dict
from typing import List

from dynaconf import Validator

GLOBAL_DEFAULTS: Dict[str, Any] = {}

validators: List[Validator] = [
    Validator("version", **GLOBAL_DEFAULTS),
    Validator(
        "server.ip", "server.api_path", "server.port", "server.url", **GLOBAL_DEFAULTS
    ),
    Validator("jwt.algorithm", "jwt.access_token_expire_minutes", **GLOBAL_DEFAULTS),
    Validator(
        "spotify.scope",
        "spotify.client_id",
        "spotify.client_secret",
        "spotify.redirect_uri",
        **GLOBAL_DEFAULTS
    ),
    Validator("database.uri", "database.db", **GLOBAL_DEFAULTS),
]
