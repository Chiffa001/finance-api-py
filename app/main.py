from fastapi import FastAPI
from asyncio import run
from app.core.database import engine
from app.models import BaseModel
from app.routes import users, operations

app = FastAPI()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

if __name__ == "__main__":
    run(init_models())


app.include_router(users.router)
app.include_router(operations.router)
