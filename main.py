# uvicorn main:app --reload

import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env").replace("\core", "")
if os.path.exists (dotenv_path):
    load_dotenv (dotenv_path)

USER=os.getenv("DATABASE_USER")
NAME=os.getenv("DATABASE_NAME")
HOST=os.getenv("DATABASE_HOST")
PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL_AIOPG = f"postgresql+aiopg://{USER}:{PASSWORD}@{HOST}/{NAME}"
DATABASE_URL_ASYNCPG = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{NAME}?ssl=true"

database = databases.Database(DATABASE_URL_AIOPG)

metadata = sqlalchemy.MetaData()

engine = create_async_engine(
    DATABASE_URL_ASYNCPG
)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "all done!!!"}