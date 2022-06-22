from pydantic import BaseModel


class TokenRead(BaseModel):
    access_token: str