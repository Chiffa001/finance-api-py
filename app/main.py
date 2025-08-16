from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import users, operations

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(operations.router)
