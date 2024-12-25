from pydantic import BaseModel


class TokenSchema(BaseModel):
    sub: str
    exp: int

class AuthDto(BaseModel):
    login: str
    password: str

class SystemUser(BaseModel):
    id: int
    telegram_id: int
    login: str
    hash_password: str


