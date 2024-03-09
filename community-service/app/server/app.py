import os
import httpx

from time import sleep
from redis import Redis

from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.server.routes.community import router as CommunityRouter
from app.server.routes.post import router as PostRouter
from app.server.routes.member import router as MemberRouter
from app.server.routes.application import router as ApplicationRouter
from app.server.routes.comment import router as CommentRouter


def include_router(app):
    app.include_router(CommunityRouter, tags=["Community"], prefix="/community")
    app.include_router(MemberRouter, tags=["Member"], prefix="/member")
    app.include_router(PostRouter, tags=["Post"], prefix="/post")
    app.include_router(ApplicationRouter, tags=["Application"], prefix="/application")
    app.include_router(CommentRouter, tags=["Comment"], prefix="/comment")

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

origins = [
    "http://buidl2.vercel.com",
    "http://localhost:3000",
    # 필요한 경우 추가 출처
]

# 모든 출처를 허용하는 CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # 모든 출처 허용
    allow_origins=origins,  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}



@app.on_event("startup")
async def startup_client():
    redis_flag = False
    redis_delay = 15
    while redis_flag == False:
        redis_host = os.getenv("REDIS_HOST","redis")
        r = Redis(redis_host, socket_connect_timeout=1) # short timeout for the test
        try:
            redis_flag = r.ping()
        except Exception as e:
            print("Redis ping has error", e, flush=True)

        if redis_flag == False:
            print(f"Redis is not Ready yet try again {redis_delay} seconds later", flush=True)
            sleep(redis_delay)

    metacommunity_delay = 30
    metacommunity_flag = False
    response = None
    while metacommunity_flag == False:
        async with httpx.AsyncClient() as client:
            metacommunity_host = os.getenv("ORM_METACOMMUNITY_SERVICE", 
                                        "http://orm-metacommunity-service:8006")
            try:            
                response = await client.get(f'{metacommunity_host}',timeout=3)
            except httpx.HTTPError as exc:
                print(f"HTTP error: {exc}")

            if response is not None:
                print(response.status_code, flush=True)
                metacommunity_flag = True if response.status_code == 200 else False
            else:
                print(f"Service is not Ready yet try again {metacommunity_delay} seconds later", flush=True)
                sleep(metacommunity_delay)

