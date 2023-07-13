from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config.config import settings

from app.server.routes.member import router as MemberRouter

def include_router(app):
    app.include_router(MemberRouter, tags=["Member"], prefix="/member")

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
    mongodb_flag = False
    mongodb_delay = 30
    while mongodb_flag == False:
        client = MongoClient(settings.DATABASE_URI, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        try:
            info = client.server_info() # Forces a call.
        except ServerSelectionTimeoutError:
            print(f"MongoDB is not Ready yet try again {mongodb_delay} seconds later", flush=True)
    client.close()
    
    app.mongodb_client = MongoClient(settings.DATABASE_URI)
    app.database = app.mongodb_client[settings.DATABASE_MEMBER]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}