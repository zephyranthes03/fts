import os
from time import sleep
from redis import Redis
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
    redis_flag = False
    mongodb_flag = False
    redis_delay = 15
    mongodb_flag = 30
    while redis_flag == False:
        redis_host = os.getenv("REDIS_HOST","redis")
        r = Redis(redis_host, socket_connect_timeout=1) # short timeout for the test

        r.ping()         
        sleep(redis_delay)





    pass
    #await load_symptom_indexes()
    

