from contextlib import asynccontextmanager

import asyncpg
from asyncpg import Pool
from fastapi import FastAPI

from app.config import config

url = config.DB_URL

class Database:
    def __init__(self, url):
        self.url: str = url
        self.pool: Pool | None = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.url)

    async def close(self):
        await self.pool.close()

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)


db = Database(url)

async def connect():
    await db.connect()
    print("Connected to database")

async def disconnect():
    await db.close()
    print("Disconnected from database")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()