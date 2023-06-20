from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from app.config.config import settings

from app.server.routes.symptom_index import router as Symptom_indexRouter
from app.server.routes.disease import router as DiseaseRouter
from app.server.routes.diagnosis import router as DiagnosisRouter

def include_router(app):
    app.include_router(Symptom_indexRouter, tags=["Symptom_index"], prefix="/symptom_index")
    app.include_router(DiagnosisRouter, tags=["Diagnosis"], prefix="/diagnosis")
    app.include_router(DiseaseRouter, tags=["Disease"], prefix="/disease")

# def configure_static(app):
#     app.mount("/static", StaticFiles(directory="static"), name="static")

# def create_tables():
#     print(Base.metadata.tables,flush=True)
#     if len(Base.metadata.tables)==0:
#         Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI()
    include_router(app)
    # configure_static(app)
    # create_tables()
    return app


app = start_application()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DATABASE_URI)
    app.database = app.mongodb_client[settings.SYMPTOM_DATABASE_NAME]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}