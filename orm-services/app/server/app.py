from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from time import sleep
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config.config import settings

from app.server.routes.symptom_index import router as Symptom_indexRouter
from app.server.routes.disease import router as DiseaseRouter
from app.server.routes.diagnosis import router as DiagnosisRouter

from app.server.routes.board import router as BoardRouter
from app.server.routes.community import router as CommunityRouter

from app.server.routes.comment import router as CommentRouter

from app.server.routes.log_community import router as LogCommunityRouter

from app.server.routes.member import router as MemberRouter
from app.server.routes.application import router as ApplicationRouter

from app.server.routes.message import router as MessageRouter

from app.server.routes.post import router as PostRouter

def include_router(app):
    app.include_router(Symptom_indexRouter, tags=["Symptom_index"], prefix="/symptom_index")
    app.include_router(DiagnosisRouter, tags=["Diagnosis"], prefix="/diagnosis")
    app.include_router(DiseaseRouter, tags=["Disease"], prefix="/disease")

    app.include_router(BoardRouter, tags=["Board"], prefix="/board")
    app.include_router(CommunityRouter, tags=["Community"], prefix="/community")

    app.include_router(CommentRouter, tags=["Comment"], prefix="/comment")

    app.include_router(LogCommunityRouter, tags=["Log_Community"], prefix="/log/community")

    app.include_router(MemberRouter, tags=["Member"], prefix="/member")
    app.include_router(ApplicationRouter, tags=["Application"], prefix="/application")

    app.include_router(MessageRouter, tags=["Message"], prefix="/message")

    app.include_router(PostRouter, tags=["Post"], prefix="/post")

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
    client = None
    while mongodb_flag == False:
        client = MongoClient(settings.DATABASE_URI, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        try:
            mongodb_flag = client.server_info() # Forces a call.
        except ServerSelectionTimeoutError:
            print(f"MongoDB is not Ready yet try again {mongodb_delay} seconds later", flush=True)
        if mongodb_flag == False:
            sleep(mongodb_delay)
    client.close()
    print(f"MongoDB is Ready", flush=True)

    app.mongodb_client = MongoClient(settings.DATABASE_URI)
    app.database = app.mongodb_client[settings.DATABASE_POST]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}