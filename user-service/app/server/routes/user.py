from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.process.process import (
    read_users,
    read_user_by_id,
    delete_user,
    add_user,
    update_user
)


from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
)

router = APIRouter()


@router.post("/", response_description="User data folder added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    print(user['email'],flush=True)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.put("/", response_description="User data folder Updated into the database")
async def update_user_data(id: str, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    print(user['email'],flush=True)
    update_user = await update_user(id, user)
    return ResponseModel(update_user, "User updated successfully.")

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await read_users()
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/{id}", response_description="Users retrieved")
async def get_users(id:str):
    users = await read_user_by_id(id)
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id:str):
    deleted_user = await delete_user(id)
    if deleted_user == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )