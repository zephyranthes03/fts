from pydantic import BaseModel

from fastapi import FastAPI

from app.server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}