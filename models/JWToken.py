from pydantic import BaseModel

class JWToken(BaseModel):
    access_token: str
    token_type: str