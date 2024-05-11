from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from time import sleep
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config.config import settings

from app.server.routes.board import router as BoardRouter
from app.server.routes.community import router as CommunityRouter
from app.server.util.logging import logger

def include_router(app):
    app.include_router(BoardRouter, tags=["Board"], prefix="/board")
    app.include_router(CommunityRouter, tags=["Community"], prefix="/community")

# def configure_static(app):
#     app.mount("/static", StaticFiles(directory="static"), name="static")

# def create_tables():
#     logger.info(Base.metadata.tables)
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
    client = None
    while mongodb_flag == False:
        client = MongoClient(settings.DATABASE_URI, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        try:
            mongodb_flag = client.server_info() # Forces a call.
        except ServerSelectionTimeoutError:
            logger.info(f"MongoDB is not Ready yet try again {mongodb_delay} seconds later", )
        if mongodb_flag == False:
            sleep(mongodb_delay)
    client.close()
    logger.info(f"MongoDB is Ready", )

    app.mongodb_client = MongoClient(settings.DATABASE_URI)
    app.database = app.mongodb_client[settings.DATABASE_METACOMMUNITY]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}