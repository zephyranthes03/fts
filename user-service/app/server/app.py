from pydantic import BaseModel

from fastapi import FastAPI, Request

# from starlette.middleware.sessions import SessionMiddleware
from app.server.routes.user import router as UserRouter
import redis


app = FastAPI()

# # Create a Redis client
# redis_client = redis.Redis(host="redis", port=6379, db=0)

# # Create the FastAPI application and add the SessionMiddleware
# app.add_middleware(
#     SessionMiddleware, 
#     secret_key="some-secret-key",
#     session_backend=RedisSessionBackend(client=redis_client)
# )


app.include_router(UserRouter, tags=["User"], prefix="/user")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}

@app.post("/save")
async def save_session_data(request: Request, key: str, value: str):
    # Save data to the session
    request.session[key] = value
    return {"detail": "Data saved to session"}

@app.get("/read/{key}")
async def read_session_data(request: Request, key: str):
    # Read data from the session
    value = request.session.get(key)
    return {"key": key, "value": value}

@app.delete("/delete/{key}")
async def delete_session_data(request: Request, key: str):
    # Delete data from the session
    if key in request.session:
        del request.session[key]
        return {"detail": f"{key} deleted from session"}
    else:
        return {"detail": f"No {key} found in session"}

