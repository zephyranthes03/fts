from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
    add_user,
    retrieve_user_by_id,
    retrieve_user_by_social_email,
    retrieve_user_by_email_password,
    retrieve_users,
    delete_user,
    update_user,
    set_password,
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
    SocialEmailSchema,
    EmailSchema,
)

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user['password'] = str(await set_password(user['password']))
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/id/{id}", response_description="User data retrieved by user_id")
async def get_user_data(id: str):
    user = await retrieve_user_by_id(id)
    if 'data' in user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.post("/social_email/", response_description="User data retrieved by social email")
async def get_user_data_social_email(socialEmail: SocialEmailSchema = Body(...)):
    socialEmail = jsonable_encoder(socialEmail)
    user = await retrieve_user_by_social_email(socialEmail)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.post("/email/", response_description="User data retrieved by email and password")
async def get_user_data_email_password(email: EmailSchema = Body(...)):
    email = jsonable_encoder(email)
    email['password'] = str(await set_password(email['password']))

    print(email,flush=True)
    user = await retrieve_user_by_email_password(email)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.put("/id/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    req['password'] = str(await set_password(req['password']))
    user = jsonable_encoder(req)
    updated_user = await update_user(id, user)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/id/{id}", response_description="User data deleted from the database")
async def delete_user_data(id:str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel([], "Empty list returned")
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )