from models.JWToken import JWToken

TEST_ACCESS_TOKEN = "hello there"
TEST_TOKEN_TYPE  = "general kenobi"

def test_JWToken():
    jwt: JWToken = JWToken(access_token=TEST_ACCESS_TOKEN,token_type=TEST_TOKEN_TYPE)

    assert jwt.access_token == TEST_ACCESS_TOKEN
    assert jwt.token_type == TEST_TOKEN_TYPE

    assert len(jwt.dict().keys()) == 2
