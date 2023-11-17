from fastapi import FastAPI, Depends, APIRouter, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from datetime import datetime, timedelta
from starlette.responses import JSONResponse

import httpx

router = APIRouter()

#router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

NAVER_CLIENT_ID = "8TU3gk6Sfxq9i2gxLX7Z"
NAVER_CLIENT_SECRET = "zoUqpjzdv5"
KAKAO_CLIENT_ID = "f6124cdaf153e3f7bd71349e832279f9"
GOOGLE_CLIENT_ID_PREFIX = "855018704830-hrvjk7hj51ennokqrfi1t0ug1i6aj0k9"
GOOGLE_CLIENT_ID = f"{GOOGLE_CLIENT_ID_PREFIX}.apps.googleusercontent.com"

NAVER_CALLBACK_URL = "https://imgroo.kr/naver/callback"
KAKAO_CALLBACK_URL = "https://imgroo.kr/kakao/callback"
GOOGLE_CALLBACK_URL = "https://imgroo.kr/google/callback"
SERVICE_URL = "https://imgroo.kr"

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {
                                                        "NAVER_CLIENT_ID": NAVER_CLIENT_ID, 
                                                        "KAKAO_CLIENT_ID": KAKAO_CLIENT_ID, 
                                                        "GOOGLE_CLIENT_ID_PREFIX": GOOGLE_CLIENT_ID_PREFIX,
                                                        "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID, 
                                                        "NAVER_CALLBACK_URL": NAVER_CALLBACK_URL,
                                                        "KAKAO_CALLBACK_URL": KAKAO_CALLBACK_URL,
                                                        "GOOGLE_CALLBACK_URL": GOOGLE_CALLBACK_URL,
                                                        "request": request,
                                                        "SERVICE_URL": SERVICE_URL})

@router.get("/callback")
async def callback(request: Request):
    return templates.TemplateResponse("naver/callback.html", {"CLIENT_ID": NAVER_CLIENT_ID, 
                                                        "CALLBACK_URL": NAVER_CALLBACK_URL,
                                                        "request": request})

# https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id=jyvqXeaVOVmV&client_secret=527300A0_COq1_XV33cf&refresh_token=c8ceMEJisO4Se7uGCEYKK1p52L93bHXLn
# https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id=jyvqXeaVOVmV&client_secret=527300A0_COq1_XV33cf&access_token=c8ceMEJisO4Se7uGCEYKK1p52L93bHXLnaoETis9YzjfnorlQwEisqemfpKHUq2gY&service_provider=NAVER
@router.get("/logout")
async def logout(access_token: str):
    async with httpx.AsyncClient() as client:
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        params = {
            'grant_type': 'delete',
            'client_id': NAVER_CLIENT_ID,
            'client_secret': NAVER_CLIENT_SECRET,
            'service_provider': 'NAVER',
            'access_token': access_token,
        }
        r = await client.get(f'https://nid.naver.com/oauth2.0/token', params=params) 
        data = r.json() #['data']
        print(data,flush=True) 
            