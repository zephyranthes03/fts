import os
import httpx

from time import sleep
from redis import Redis

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
    redis_flag = False
    redis_delay = 15
    while redis_flag == False:
        redis_host = os.getenv("REDIS_HOST","redis")
        r = Redis(redis_host, socket_connect_timeout=1) # short timeout for the test
        redis_flag = r.ping()
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

