from typing import Optional

from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    create_date: str = Field(...)
    community: str = Field(...)
    phone: str = Field(...)
    email_acceptance: str = Field(...)
    message_acceptance: str = Field(...)
    user_type: str = Field(...)
    expire_time: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "19850109",
                "email": "john_doe@gmail.com",
                "password": "test",
                "create_date": "19850109",
                "community": "{'acne':{'grade':'user','status':'early'}}",
                "phone": "72065122567",
                "email_acceptance": "all",
                "message_acceptance": "community|system",
                "user_type": "user",
                "expire_time": 30
            }
        }

class SocialEmailSchema(BaseModel):
    email: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "john_doe@gmail.com",
            }
        }   

class EmailSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "john_doe@gmail.com",
                "password": "test",
            }
        }        


class UpdateUserModel(BaseModel):
    email: Optional[str]
    password: Optional[str]
    create_date: Optional[str]
    community: Optional[str]
    phone: Optional[str]
    email_acceptance: Optional[str]
    message_acceptance: Optional[str]
    user_type: Optional[str]
    expire_time: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "email": "john_doe@gmail.com",
                "password": "test",
                "create_date": "19850109",
                "community": "{'acne':{'grade':'user','status':'early'}}",
                "phone": "USC00332098",
                "email_acceptance": "all",
                "message_acceptance": "community|system",
                "user_type": "user",
                "expire_time": 30
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}