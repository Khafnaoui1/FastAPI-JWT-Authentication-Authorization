from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.util.init_db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Created")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "Running..."}