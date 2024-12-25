import asyncio
import json
import aiohttp
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from starlette import status
from ..utils.crypto_url.crypto import decrypt_url, encrypt_url
from ..database.redis_client import client
from ..schemas.movie import MovieInfo


router = APIRouter()

ORIGIN, REFERRER = 'https://stage.player.cdnvideohub.com', 'https://stage.player.cdnvideohub.com/'


@router.get('/video_url')
async def get_video_url(id: str):
    url = await client.get(id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL is not exists"
        )
    result = json.loads(url)
    result = MovieInfo(**result)
    result.url = encrypt_url(result.url)
    return result


@router.get("/stream")
async def stream_video(url: str):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': ORIGIN,
        'Pragma': 'no-cache',
        'Referer': REFERRER,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    url = decrypt_url(url)
    async def get_content_length():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    length = response.headers.get('Content-Length')
        except asyncio.TimeoutError:
            print(f"Timeout error while downloading: {url}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        return length

    async def video_stream():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk
        except asyncio.TimeoutError:
            print(f"Timeout error while downloading: {url}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise


    return StreamingResponse(video_stream(), media_type="video/mp4", headers={"Accept-Ranges": "bytes", "Content-Length": await get_content_length()})

