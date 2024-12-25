from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..deps.dependencies import get_current_user
from ..schemas.auth_user import SystemUser
from ..database.redis_client import client
from ..database.models.models import LogFilms



router = APIRouter(prefix='/dashboard')


@router.get('/downloads')
async def get_downloads(user: SystemUser = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    all_keys = await client.keys()
    all_data = {}
    if all_keys:
        for key in all_keys:
            value = await client.get(key)
            if not isinstance(value, list):
                all_data[key] = await client.get(key)
    print(all_data)
    return all_data

@router.get('/statistics')
async def get_users(user: SystemUser = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    logs = await LogFilms.all()
    count = len(logs)
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    logs_today = await LogFilms.filter(downloaded_at__range=(today_start, today_end))
    return {'count': count, 'count_today': len(logs_today)}


