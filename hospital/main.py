from fastapi import FastAPI
from routers import hospital_router, department_router
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


@app.on_event("startup")
async def startup() -> None:
    print('Connecting to db...')
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    print('Connected!')


@app.on_event("shutdown")
async def shutdown() -> None:
    print('Disconnecting from db...')
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
    print('Disconnected!')
