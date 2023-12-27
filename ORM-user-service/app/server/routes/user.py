from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List


from app.server.database.database import (
    add_user,
    retrieve_user_by_id,
    retrieve_user_by_email,
    retrieve_user_by_social_email,
    retrieve_user_by_email_password,
    retrieve_users,
    delete_user,
    update_user,
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
    SocialEmailSignupSchema,
    SocialEmailLoginSchema,
    EmailSchema,
)

from app.server.util.encrypt import (
    set_password,
    check_password_hash
)

from app.server.util.convert import user_from_str, user_to_str, social_user_to_userSchema

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user = await user_to_str(user)
    # print(user,flush=True)

    user['password'] = str(await set_password(user['password']))
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    users_list = list()
    if users:
        for user in users:
            user_dict = await user_from_str(user)
            users_list.append(user_dict)

        return users_list
    return users_list

@router.get("/id/{id}", response_description="User data retrieved by user_id")
async def get_user_data_by_id(id: str):
    user = await retrieve_user_by_id(id)
    user_dict = dict()
    if user:
        user_dict = await user_from_str(user)
        return user_dict
    return user_dict

@router.get("/email/{email}", response_description="User data retrieved by email")
async def get_user_data_by_email(email: str):
    user = await retrieve_user_by_email(email)
    user_dict = dict()
    if user:
        user_dict = await user_from_str(user)
        return user_dict
    return user_dict

@router.post("/social_email_login", response_description="User data retrieved by social email")
async def get_user_data_social_email(socialEmail: SocialEmailLoginSchema = Body(...)):
    socialEmail = jsonable_encoder(socialEmail)
    user = await retrieve_user_by_social_email(socialEmail)
    user_dict = dict()
    if user:
        user_dict = await user_from_str(user)
        return user_dict
    return user_dict

@router.post("/social_email_signup", response_description="User data signup by social email")
async def get_user_data_social_email(socialEmail: SocialEmailSignupSchema = Body(...)):
    socialEmail = jsonable_encoder(socialEmail)
    user_dict = dict()
    user = await retrieve_user_by_social_email(socialEmail)
    action_type = "Login"
    if len(user) == 0:
        userSchema = await social_user_to_userSchema(socialEmail)
        added_user = await add_user_data(userSchema)
        user = await retrieve_user_by_social_email(socialEmail)
        signup_flag = "Signup"
    if user:
        user_dict = await user_from_str(user)
        user_dict["action"] = action_type
    return user_dict

@router.post("/email/", response_description="User data retrieved by email and password")
async def get_user_data_email_password(email: EmailSchema = Body(...)):
    email = jsonable_encoder(email)
    email['password'] = str(await set_password(email['password']))
    user = await retrieve_user_by_email_password(email)
    user_dict = dict()
    if user:
        user_dict = await user_from_str(user)
        return user_dict
    return user_dict

@router.put("/email/{email}")
async def update_user_data(email: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    req = await user_to_str(req)
    if 'password' in req:
        req['password'] = str(await set_password(req['password']))
    else:
        user_data = await retrieve_user_by_email(email)
        # user_data_dict = jsonable_encoder(user_data)
        # print(user_data_dict,flush=True)
        req['password'] = user_data[1]
    user = jsonable_encoder(req)
    updated_user = await update_user(email, user)
    if updated_user:
        return ResponseModel(
            "User with Email: {} update is successful".format(email),
            "User updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/email/{email}", response_description="User data deleted from the database")
async def delete_user_data(email:str):
    deleted_user = await delete_user(email)
    if deleted_user:
        return ResponseModel([], "Empty list returned")
    return ErrorResponseModel(
        "An error occurred", 404, "User with email {0} doesn't exist".format(id)
    )