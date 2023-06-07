from pydantic import BaseModel

from fastapi import FastAPI

from app.server.routes.disease import router as DiseaseRouter
from app.server.routes.image import router as ImageRouter
from app.server.routes.diag import router as DiagRouter

app = FastAPI()

app.include_router(DiseaseRouter, tags=["Disease"], prefix="/disease")
app.include_router(ImageRouter, tags=["Image"], prefix="/image")
app.include_router(DiagRouter, tags=["Diag"], prefix="/diag")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}