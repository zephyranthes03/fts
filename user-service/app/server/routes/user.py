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
    update_user,
    test_func
)


from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,    
    SocialEmailSchema,
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


@router.post("/", response_description="User data folder added into the database")
async def add_user_data(user: UserSchema = Body(...), dependencies:dict=Depends(verify_token)):
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
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

# @router.get("/id/{id}", response_description="Users retrieved by id")
# async def get_user_by_id(id:str, dependencies:dict=Depends(verify_token)):
#     users = await read_user_by_id(id)
#     if users:
#         return ResponseModel(users, "Users data statistic retrieved successfully")
#     return ResponseModel(users, "Empty list returned")

@router.get("/email/{email}", response_description="Users retrieved by email")
async def get_user_by_email(email:str, dependencies:dict=Depends(verify_token)):
    users = await read_user_by_email(email)
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

    
# Login by Social Email
@router.post("/social_email", response_description="Users retrieved by social email")
async def post_user_social_email(socialEmail: SocialEmailSchema = Body(...)):
    socialEmail = jsonable_encoder(socialEmail)
    user = await read_user_by_social_email(socialEmail)
    if user:
        await session_create(user)
        if user['data']:
            print(user['data'], flush=True)
            return ResponseModel(user, "User data retrieved successfully")
        else:
            return ErrorResponseModel("Return dict is Empty", 400, 'User data retrieved failure')
    return ErrorResponseModel("Return data requests failure", 400, "Login Failure")

# Login by Email
@router.post("/email", response_description="User data retrieved by email and password")
async def get_user_data(email: EmailSchema = Body(...)):
    email = jsonable_encoder(email)
    user = await read_user_by_email_password(email)
    if user['data']:
        print("print_from email",flush=True)
        print(user,flush=True)
        await session_create(user)
        return ResponseModel(user, "User data retrieved successfully")
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