
def test_config():
    from config import settings

    assert settings.jwt.algorithm == "HS256"