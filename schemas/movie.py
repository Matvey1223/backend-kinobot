from typing import Optional

from pydantic import BaseModel

class MovieInfo(BaseModel):
    url: str
    title: str
    image: Optional[str] = None