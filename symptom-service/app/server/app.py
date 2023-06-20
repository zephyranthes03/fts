from pydantic import BaseModel

from fastapi import FastAPI

from app.server.routes.disease import router as DiseaseRouter
from app.server.routes.diagnosis import router as DiagnosisRouter
from app.server.routes.symptom_index import router as Symptom_indexRouter

from app.server.routes.symptom_index import load_symptom_indexes

app = FastAPI()

app.include_router(DiseaseRouter, tags=["Disease"], prefix="/disease")
app.include_router(DiagnosisRouter, tags=["Diagnosis"], prefix="/diagnosis")
app.include_router(Symptom_indexRouter, tags=["Symptom_index"], prefix="/symptom_index")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}

@app.on_event("startup")
async def startup_client():
    pass
    #await load_symptom_indexes()
    

