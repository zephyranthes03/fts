from pydantic import BaseModel

from fastapi import FastAPI

from app.server.routes.community import router as CommunityRouter

app = FastAPI()

app.include_router(CommunityRouter, tags=["Community"], prefix="/community")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}

@app.on_event("startup")
async def startup_client():
    pass
    #await load_symptom_indexes()
    

