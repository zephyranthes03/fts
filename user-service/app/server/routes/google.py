from fastapi import FastAPI, Depends, APIRouter, Request, HTTPException, status, Cookie
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.server.util.util import cast_to_number
from starlette.responses import JSONResponse
from starlette.requests import Request
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import Depends
from fastapi.security import OpenIdConnect
from starlette.responses import RedirectResponse


from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel  
)

# from jose import jwt
import jwt
import httpx
import os 

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID_PREFIX = "855018704830-hrvjk7hj51ennokqrfi1t0ug1i6aj0k9"
GOOGLE_CLIENT_ID = "855018704830-hrvjk7hj51ennokqrfi1t0ug1i6aj0k9.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
# Configure Google provider

GOOGLE_REDIRECT_TOKEN_URI = "https://imgroo.kr/google/token"
GOOGLE_REDIRECT_LOGIN_URL_OLD = "https://imgroo.kr/google/auth_login"
GOOGLE_REDIRECT_SIGNUP_URL_OLD = "https://imgroo.kr/google/auth_signup"
GOOGLE_REDIRECT_LOGIN_URL = "https://imgroo.kr/google/callback_login"
GOOGLE_REDIRECT_SIGNUP_URL = "https://imgroo.kr/google/callback_signup"

# Configuration
API_SECRET_KEY = os.environ.get('API_SECRET_KEY') or None
API_SECRET_KEY = "TESTTESTTEST"
if API_SECRET_KEY is None:
    raise BaseException('Missing API_SECRET_KEY env var.')
API_ALGORITHM = os.environ.get('API_ALGORITHM') or 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


@router.get("/social_login", response_description="Google login URL link")
async def social_login():
    #print(f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_LOGIN_URL}&scope=openid%20profile%20email&access_type=offline",flush=True)
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_LOGIN_URL_OLD}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/social_signup", response_description="Google signup URL link")
async def social_signup():
    #print(f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_SIGNUP_URL}&scope=openid%20profile%20email&access_type=offline",flush=True)
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_SIGNUP_URL_OLD}&scope=openid%20profile%20email&access_type=offline"
    }


@router.post("/callback_login")
async def google_callback_login(request: Request):
    # Extract the token from the request
    form_data = await request.form()
    token = form_data.get('credential')

    if not token:
        raise HTTPException(status_code=400, detail="Missing Google token")

    # Validate the token and retrieve user info
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')

        if user_info_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")
        user_info = user_info_response.json()

        json_payload = {
            'email' : user_info['email'],
            'login_type' : 'google',
            'access_token': token,
            'refresh_token': ""
        }
        print(json_payload,flush=True)
        res = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_login', json=json_payload) 
        result = res.json()
        return ResponseModel("Social User", "Login Social User successfully")


@router.post("/callback_signup")
async def google_callback_signup(request: Request):
    # Extract the token from the request
    form_data = await request.form()
    token = form_data.get('credential')

    if not token:
        raise HTTPException(status_code=400, detail="Missing Google token")

    # Validate the token and retrieve user info
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')

        if user_info_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")
        user_info = user_info_response.json()

        json_payload = {
            'email' : user_info['email'],
            'login_type' : 'google',
            'extra_data' :  {
                'id' : user_info['id'],
                'username' : user_info['name'],
                'nickname' : user_info['email'],
                'age' : user_info['age_range'] if 'age_range' in user_info else "empty",
                'gender' : user_info['gender'] if 'gender' in user_info else "empty",
            },
            'access_token': token,
            'refresh_token': ""
        }
        print(json_payload,flush=True)
        res = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_signup', json=json_payload) 
        result = res.json()
        return ResponseModel("Social User", "Signup Social User successfully")
    
@router.get("/auth_login", response_description="Google login URL link", response_model=None)
async def auth_login(code: str)-> ResponseModel: # (code:str, scope:str, authuser:int, prompt:str):

    token_url = "https://accounts.google.com/o/oauth2/token"
    # print(request,flush=True)
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_LOGIN_URL,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        #response = requests.post(token_url, data=data)
        print(response.json(),flush=True)
        access_token = response.json().get("access_token")
        refresh_token = "" if "refresh_token" not in response.json() else response.json().get("refresh_token") 
        print(access_token, flush=True)
        print("refresh_token", flush=True)
        user_info = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        user_param = user_info.json()
        print(user_param, flush=True)
        json_payload = {
            'email' : user_param['email'],
            'login_type' : 'google',
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        print(json_payload,flush=True)
        res = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_login', json=json_payload) 
        result = res.json()
        return ResponseModel("Social User", "Login Social User successfully")

@router.post("/auth_signup", response_description="Google signup URL link", response_model=None) 
async def auth_signup(code: str): #, scope:str, authuser:int, prompt:str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_SIGNUP_URL,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        #response = requests.post(token_url, data=data)
        print(response.json(),flush=True)
        access_token = response.json().get("access_token")
        refresh_token = "" if "refresh_token" not in response.json() else response.json().get("refresh_token") 
        print(access_token, flush=True)
        print("refresh_token", flush=True)
        user_info = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        user_param = user_info.json()
        print(user_param, flush=True)
        json_payload = {
            'email' : user_param['email'],
            'login_type' : 'google',
            'extra_data' :  {
                'id' : user_param['id'],
                'username' : user_param['name'],
                'nickname' : user_param['email'],
                'age' : user_param['age_range'] if 'age_range' in user_param else "empty",
                'gender' : user_param['gender'] if 'gender' in user_param else "empty",
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        print(json_payload,flush=True)
        res = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_signup', json=json_payload) 
        result = res.json()
        # return ResponseModel("Social User", "Generate Social User successfully")
        return "Generate Social User successfully"

@router.get("/token", response_description="Google login URL token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


@router.post("/refresh", response_description="Google login URL token")
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM]) # decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    email = payload.get('sub')
                    # Validate email
                    if False: # valid_email_from_db(email): # email in FAKE_DB
                        # Create and return token
                        return JSONResponse({'result': True, 'access_token': create_token(email)})

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION




@router.get("/logout", response_description="Google logout URL link")
async def logout(access_token: str):
    async with httpx.AsyncClient() as client:
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        user_info = await client.post("https://accounts.google.com/o/oauth2/revoke", 
                                      params={'token': access_token},
                                      headers=headers)
    return user_info.json()


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


