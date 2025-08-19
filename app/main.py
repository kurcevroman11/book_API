from fastapi import FastAPI
from app.api import v1
from app.core.database import database, engine, metadata

# Создаём таблицы
# metadata.create_all(engine)

app = FastAPI(title="FastAPI MVC + DB")

app.include_router(v1.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
