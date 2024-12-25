from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pythonProject.utils.config import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from pythonProject.schemas.auth_user import SystemUser
from pythonProject.database.models.models import Admins

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl='/',
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(
                token=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )
    except(JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await Admins.filter(login = payload.get('sub'))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user