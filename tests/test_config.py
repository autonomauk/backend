import pytest
from config import settings
import os
def test_config():
    assert settings.jwt.algorithm == "HS256"

@pytest.mark.parametrize("dynaconf_env,exp",[('development',1), ('production',2)])
def test_switcher(dynaconf_env, exp):
    assert settings.from_env(dynaconf_env).server.value_for_testing == exp

    with settings.using_env(dynaconf_env):
        assert settings.server.value_for_testing == exp

    settings.setenv(dynaconf_env)
    assert settings.server.value_for_testing == exp

@pytest.mark.parametrize("dynaconf_env,exp",[('development',1), ('production',2)])
def test_switcher_via_env_var(dynaconf_env, exp):
    os.environ["ENV_FOR_DYNACONF"] = dynaconf_env
    from config import get_setting

    settings  = get_setting()

    assert settings.server.value_for_testing == exp
