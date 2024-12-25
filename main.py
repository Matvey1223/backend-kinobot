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
    allow_origins=["*"],  # Разрешить запросы отовсюду, для тестов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*", "Range"]
)

if __name__ == "__main__":
    # Устанавливаем параметры для SSL
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain(certfile="ssl_cert.pem", keyfile="ssl_key.pem")

    # Запуск на HTTPS с указанным IP и портом
    uvicorn.run(
        "pythonProject.main:app",
        host="192.168.0.106",
        port=8000,
        reload=True,
    )