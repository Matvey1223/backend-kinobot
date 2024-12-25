from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from pythonProject.utils.config import ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days



def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=60*24*7)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except JWTError:
        raise Exception("Invalid token")


