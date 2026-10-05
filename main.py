from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.routers.auth import authRouter
from app.util.init_db import create_tables
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput 


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Created")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")


@app.get("/health")
def health_check():
    return {"status": "Running..."}

@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)):
    return {"data": user}