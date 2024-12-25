import ssl

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from database.database import init_db, close
from routers import auth, admin_functions, stream
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close()

app = FastAPI(lifespan = lifespan)
app.include_router(auth.router)
app.include_router(admin_functions.router)
app.include_router(stream.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Range"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="192.168.0.106",
        port=8000,
        reload=True,
    )