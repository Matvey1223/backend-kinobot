from fastapi import APIRouter, HTTPException
from starlette import status

from ..utils.password.hashing import verify_password
from ..utils.jwt.jwt import create_access_token, create_refresh_token, decode_refresh_token
from ..schemas.auth_user import AuthDto
from ..database.models.models import Admins
from pydantic import BaseModel
from jose.exceptions import JWTError

router = APIRouter()

class RefreshDto(BaseModel):
    refresh_token: str
@router.post("/refresh-token")
async def refresh_token(refresh_token: RefreshDto):
    try:
        payload = decode_refresh_token(refresh_token.refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
        new_access_token = create_access_token(username)
        return {"access_token": new_access_token}
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: AuthDto):
    user = await Admins.filter(login = form_data.login)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user[0].hash_password
    print(hashed_pass)
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    print(3)
    return {
        "access_token": create_access_token(user[0].login),
        "refresh_token": create_refresh_token(user[0].login),
    }


