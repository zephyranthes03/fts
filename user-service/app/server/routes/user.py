from typing import Any
import httpx
import logging
from fastapi import APIRouter, Body, Depends, Request, Response, Header, HTTPException
from fastapi.encoders import jsonable_encoder

from app.server.process.process import (
    read_users,
    read_user_by_id,
    read_user_by_email,
    read_user_by_social_email,
    read_user_by_email_password,
    delete_user,
    add_user,
    signup_social_user,
    update_user,
    test_func
)


from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,    
    SocialEmailLoginSchema,
    SocialEmailSignupSchema,
    EmailSchema,    
)

from app.server.util.session import (
    session_load,
    session_update,
    session_create,
    session_delete
)


router = APIRouter()

async def verify_token(session_key: str = Header(None)):
    if session_key is None:
        raise HTTPException(status_code=400, detail="Invalid session")
    else:
        session = await session_load(session_key)

    return session


@router.post("/", response_description="User data added into the database")
async def signup_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if new_user.get('error', None):
        return ErrorResponseModel(
            new_user.get('error', None),
            500,
            new_user.get('message', None)
        )
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users(dependencies:dict=Depends(verify_token)):
    users = await read_users()
    return ResponseModel(users, "Users data statistic retrieved successfully")
    # return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

# @router.get("/id/{id}", response_description="Users retrieved by id")
# async def get_user_by_id(id:str, dependencies:dict=Depends(verify_token)):
#     users = await read_user_by_id(id)
#     if users:
#         return ResponseModel(users, "Users data statistic retrieved successfully")
#     return ResponseModel(users, "Empty list returned")

@router.get("/email/{email}", response_description="Users retrieved by email")
async def get_user_by_email(email:str, dependencies:dict=Depends(verify_token)):
    users = await read_user_by_email(email)
    return ResponseModel(users, "Users data statistic retrieved successfully")

# Login by Social Email
@router.post("/social_login", response_description="Users retrieved by social email")
async def post_user_social_login(user_form: SocialEmailLoginSchema = Body(...)):
    socialUser = jsonable_encoder(user_form)
    social_email_extract = socialUser['email']
    user = await read_user_by_social_email(socialUser)
    if not user:
        return ErrorResponseModel("Return data requests failure", 500, "Email not exist!")

    if 'email' in socialUser:
        user = await read_user_by_social_email(socialUser)
        user['access_token'] = socialUser['access_token']
        user['refresh_token'] = socialUser['refresh_token']
        user['login_type'] = socialUser['login_type']
        session = await session_create(user)
        print(session, flush=True)
        return ResponseModel(session, "User data retrieved successfully")
    
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")


@router.post("/social_signup", response_description="Social User data added into the database")
async def post_user_social_signup(user_form: SocialEmailSignupSchema = Body(...)):
    socialUser = jsonable_encoder(user_form)
    email_extract = socialUser['email']
    response_social_user_dict = dict()
    user_check_by_social_email = await read_user_by_social_email(socialUser)
    if not user_check_by_social_email:
        user_check_by_email = await read_user_by_email(email_extract)
        if user_check_by_email:
            user_check_by_email['account_type'] = user_check_by_email['account_type'].append(socialUser['login_type'])
            user_check_by_email = await update_user(email_extract, user_check_by_email)
        else:
            response_social_user_dict = await signup_social_user(socialUser)
            print("response_social_user_dict",flush=True)
            print(response_social_user_dict,flush=True)
    
    user = dict()

    user = await read_user_by_email(email_extract)
    if 'email' in socialUser:
        user['access_token'] = socialUser['access_token']
        user['refresh_token'] = socialUser['refresh_token']
        user['login_type'] = socialUser['login_type']
        session = await session_create(user)

        # Override action_type value to check action type
        session['action_type'] = response_social_user_dict['action_type'] if response_social_user_dict else 'login' 
        session['email'] = socialUser['email']
        return ResponseModel(session, "User data retrieved successfully")
    
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

# Login by Email
@router.post("/email", response_description="User data retrieved by email and password")
async def get_user_data(email: EmailSchema = Body(...)):
    email = jsonable_encoder(email)
    if email:
        user = await read_user_by_email_password(email)
        user['access_token'] = ""
        user['refresh_token'] = ""
        user['login_type'] = "email"
        print(user,flush=True)
        if 'email' in user:
            if 'email' in user['account_type']:
                if user['data']:
                    session = await session_create(user)
                    return ResponseModel(session, "User data retrieved successfully")
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

# Session close
@router.post("/disconnect", response_description="Disconnect session(Remove session data from Redis)")
async def redis_delete_session(dependencies:dict=Depends(verify_token)):
    if id in dependencies:
        return ResponseModel(session_delete(dependencies["id"]), "User session disconnected successfully")
    return ErrorResponseModel("User session is empty", 400, "mpty session returned")

# Update account
@router.put("/email/{email}")
async def update_user_data(email: str, req: UpdateUserModel = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    user = jsonable_encoder(req)
    updated_user = await update_user(email, user)
    if 'data' in updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )

# delete account
@router.delete("/email/{email}", response_description="User data deleted from the database")
async def delete_user_data(email:str, dependencies:dict=Depends(verify_token)):
    deleted_user = await delete_user(email)
    if deleted_user == True:
        return ResponseModel(email, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )


#################### 
# Test function
#################### 
@router.post("/test", response_description="Users retrieved by social login")
async def post_user_social_login(request: Request):
    try:
        output = await test_func(request)
        return {"status": "OK", "data": output}
    except Exception as err:
        logging.error(f'could not print REQUEST: {err}')
        return {"status": "ERR", "error": str(err)}