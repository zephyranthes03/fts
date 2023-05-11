from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.process.process import (
    read_users,
    read_user_by_id,
    read_user_by_social_email,
    read_user_by_email_password,
    delete_user,
    add_user,
    update_user
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


@router.post("/", response_description="User data folder added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    print(user['email'],flush=True)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await read_users()
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/id/{id}", response_description="Users retrieved")
async def get_user(id:str):
    users = await read_user_by_id(id)
    if users:
        return ResponseModel(users, "Users data statistic retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.post("/social_email", response_description="Users retrieved by social email")
async def post_user_social_email(socialEmail: SocialEmailSchema = Body(...)):
    socialEmail = jsonable_encoder(socialEmail)
    user = await read_user_by_social_email(socialEmail)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.post("/email", response_description="User data retrieved by email and password")
async def get_user_data(email: EmailSchema = Body(...)):
    email = jsonable_encoder(email)
    user = await read_user_by_email_password(email)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.put("/id/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    user = jsonable_encoder(req)
    updated_user = await update_user(id, user)
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

@router.delete("/id/{id}", response_description="User data deleted from the database")
async def delete_user_data(id:str):
    deleted_user = await delete_user(id)
    if deleted_user == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )