from tortoise import Tortoise
from ..utils.config import POSTGRES_URL

async def init_db():
    print(1)
    await Tortoise.init(
        db_url= POSTGRES_URL,
        modules={"models": ["pythonProject.database.models.models"]}
    )

async def close():
    await Tortoise.close_connections()