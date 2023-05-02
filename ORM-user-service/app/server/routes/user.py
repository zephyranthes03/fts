from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
    add_user,
    add_users,
    retrieve_users_by_station,
    retrieve_users,
    delete_user,
    update_user,
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()


@router.post("/all", response_description="User data added into the database")
async def add_user_data(user: List[UserSchema] = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_users(user)
    return ResponseModel(new_user, "User added successfully.")

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="User data retrieved by station")
async def get_user_data(id):
    users = await retrieve_users_by_station(id)
    if users:
        return ResponseModel(users, "User data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
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


@router.delete("/", response_description="User data deleted from the database")
async def delete_user_data(id:str):
    deleted_user = await delete_user(id)
    if deleted_user == True:
        return ResponseModel([], "Empty list returned")
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )