from pydantic import BaseModel

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware.sessions import SessionMiddleware
from app.server.routes.user import router as UserRouter
from app.server.routes.google import router as GoogleRouter
from app.server.routes.naver import router as NaverRouter
from app.server.routes.kakao import router as KakaoRouter

from app.server.util.session import session_load

import redis

app = FastAPI()


origins = [
    "https://imgroo.kr",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Create a Redis client
# redis_client = redis.Redis(host="redis", port=6379, db=0)

# # Create the FastAPI application and add the SessionMiddleware
# app.add_middleware(
#     SessionMiddleware, 
#     secret_key="some-secret-key",
#     session_backend=RedisSessionBackend(client=redis_client)
# )

templates = Jinja2Templates(directory="templates")

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(GoogleRouter, tags=["Google"], prefix="/google")
app.include_router(NaverRouter, tags=["Naver"], prefix="/naver")
app.include_router(KakaoRouter, tags=["Kakao"], prefix="/kakao")

@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action='' onsubmit='sendMessage(event)'>
            <input type='text' id='messageText' autocomplete='off'/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8001/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/ws/debug")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"WS Message text was: {data}")

