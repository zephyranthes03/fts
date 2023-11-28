from fastapi import FastAPI, Depends, APIRouter, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from datetime import datetime, timedelta
from starlette.responses import JSONResponse

from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel  
)

import httpx
import os 

router = APIRouter()

#router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

NAVER_CLIENT_ID = "8TU3gk6Sfxq9i2gxLX7Z"
KAKAO_CLIENT_ID = "f6124cdaf153e3f7bd71349e832279f9"
KAKAO_REST_CLIENT_ID = "4f5260580754a2f0ac2c4adbe5f177ad"
GOOGLE_CLIENT_ID_PREFIX = "855018704830-hrvjk7hj51ennokqrfi1t0ug1i6aj0k9"
GOOGLE_CLIENT_ID = f"{GOOGLE_CLIENT_ID_PREFIX}.apps.googleusercontent.com"

KAKAO_CALLBACK_LOGIN_URL = "https://imgroo.kr/kakao/callback_login"
KAKAO_CALLBACK_SIGNUP_URL = "https://imgroo.kr/kakao/callback_signup"

SERVICE_URL = "https://imgroo.kr"

# @router.get("/login")
# async def login(request: Request):

    # return templates.TemplateResponse("login.html", {
    #                                                     "NAVER_CLIENT_ID": NAVER_CLIENT_ID, 
    #                                                     "KAKAO_CLIENT_ID": KAKAO_CLIENT_ID, 
    #                                                     "GOOGLE_CLIENT_ID_PREFIX": GOOGLE_CLIENT_ID_PREFIX,
    #                                                     "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID, 
    #                                                     "NAVER_CALLBACK_URL": NAVER_CALLBACK_URL,
    #                                                     "KAKAO_CALLBACK_URL": KAKAO_CALLBACK_URL,
    #                                                     "GOOGLE_CALLBACK_URL": GOOGLE_CALLBACK_URL,
    #                                                     "request": request,
    #                                                     "SERVICE_URL": SERVICE_URL})


@router.get("/callback_login")
async def callback_login(code:str):
    async with httpx.AsyncClient() as client:
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_REST_CLIENT_ID,
            'redirect_uri': KAKAO_CALLBACK_LOGIN_URL,
            'code': code,
        }
        r = await client.post(f'https://kauth.kakao.com/oauth/token', data=data, headers=header) 
        data = r.json() #['data']
        print(data,flush=True)
        if 'access_token' in data:
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            header = {'Authorization': f'Bearer {access_token}'}
            print(access_token,flush=True)
            r = await client.get(f'https://kapi.kakao.com/v2/user/me', headers=header) 
            print(r.json(),flush=True)
            user_param = r.json()
            json_payload = {
                'email' : user_param['kakao_account']['email'],
                'login_type' : 'kakao',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            print(json_payload,flush=True)
            res = await client.post(f'{os.getenv("USER_SERVICE_DOMAIN")}/user/social_email_login', headers=header, json=json_payload) 
            result = res.text
            print(result,flush=True)
            return ResponseModel("Social User", "Generate Social User successfully")

        else:
            print("ERROR", flush=True)

@router.get("/callback_signup")
async def callback_signup(code:str):
    async with httpx.AsyncClient() as client:
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_REST_CLIENT_ID,
            'redirect_uri': KAKAO_CALLBACK_SIGNUP_URL,
            'code': code,
        }
        r = await client.post(f'https://kauth.kakao.com/oauth/token', data=data, headers=header) 
        data = r.json() #['data']
        print(data,flush=True)
        if 'access_token' in data:
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            header = {'Authorization': f'Bearer {access_token}'}
            print(access_token,flush=True)
            r = await client.get(f'https://kapi.kakao.com/v2/user/me', headers=header) 
            print(r.json(),flush=True)
            user_param = r.json()
            json_payload = {
                'email' : user_param['kakao_account']['email'],
                'login_type' : 'kakao',
                'extra_data' :  {
                    'id' : user_param['id'],
                    'username' : user_param['kakao_account']['profile']['nickname'],
                    'nickname' : user_param['kakao_account']['profile']['nickname'],
                    'age' : user_param['kakao_account']['age_range'],
                    'gender' : user_param['kakao_account']['gender']
                },
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            print(json_payload,flush=True)
            res = await client.post(f'{os.getenv("USER_SERVICE_DOMAIN")}/user/social_email_signup', headers=header, json=json_payload) 
            result = res.text
            print(result,flush=True)
            return ResponseModel("Social User", "Generate Social User successfully")

        else:
            print("ERROR", flush=True)


@router.get("/logout")
async def logout(access_token: str):
    async with httpx.AsyncClient() as client:
        header = {"Content-Type": "application/x-www-form-urlencoded",
                  "Authorization": f"Bearer {access_token}" }
        res = await client.get(f'https://kauth.kakao.com/oauth/logout?client_id={KAKAO_REST_CLIENT_ID}&logout_redirect_uri={SERVICE_URL}', headers=header) 
        print(res.text,flush=True)
        return ResponseModel("Social User", "Logout Social User successfully")
