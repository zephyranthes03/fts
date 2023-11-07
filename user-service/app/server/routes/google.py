from fastapi import FastAPI, Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer
import requests
from datetime import datetime

# from jose import jwt
import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = "855018704830-hrvjk7hj51ennokqrfi1t0ug1i6aj0k9.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "https://imgroo.kr/google/auth"

@router.get("/google/login", response_description="Google login URL link")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.post("/google/auth", response_description="Google login URL link")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()

@router.post("/google/token", response_description="Google login URL token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


# @router.post("/google/token", response_description="Google login URL token")
# async def refresh(request: Request):
#     try:
#         # Only accept post requests
#         if request.method == 'POST':
#             form = await request.json()
#             if form.get('grant_type') == 'refresh_token':
#                 token = form.get('refresh_token')
#                 payload = decode_token(token)
#                 # Check if token is not expired
#                 if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
#                     email = payload.get('sub')
#                     # Validate email
#                     if valid_email_from_db(email):
#                         # Create and return token
#                         return JSONResponse({'result': True, 'access_token': create_token(email)})

#     except Exception:
#         raise CREDENTIALS_EXCEPTION
#     raise CREDENTIALS_EXCEPTION


