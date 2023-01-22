import os
from fastapi import FastAPI, Request, Response
from routers import hospital_router, department_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from db import database, metadata
# import sqlalchemy
app = FastAPI()


app.state.database = database
# """ Tables creating ( if you dont use alembic ) """
# engine = sqlalchemy.create_engine(
#     "mysql+pymysql://root:87dima87@localhost:3306/new_hospital")
# metadata.create_all(engine)

app.include_router(router=hospital_router.hospital_router,
                   prefix='/hospital',
                   tags=['Hospital'])
app.include_router(router=department_router.department_router,
                   prefix='/department',
                   tags=['Department'])

REDIS_URL = "redis://127.0.0.1:6379"

# TODO: write logs


@app.on_event("startup")
async def startup() -> None:
    print('Connecting to db...')
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    print('Connected!')
    redis = aioredis.from_url(
        REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="hospital-cache")


@app.on_event("shutdown")
async def shutdown() -> None:
    print('Disconnecting from db...')
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
    print('Disconnected!')
