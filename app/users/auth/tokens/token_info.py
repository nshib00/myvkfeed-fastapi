from pydantic import BaseModel


ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    type: str = 'Bearer'