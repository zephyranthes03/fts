from typing import Optional

from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    create_date: str = Field(...)
    community: str = Field(...)
    phone: str = Field(...)
    email_acceptance: int = Field(...)
    message_acceptance: int = Field(...)
    status: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "1981904",
                "email": "john_doe@gmail.com",
                "password": "",
                "create_date": "19850109",
                "community": "USC00332098",
                "phone": "USC00332098",
                "email_acceptance": -11,
                "message_acceptance": -140,
                "status": "user",
            }
        }


class UpdateUserModel(BaseModel):
    id: Optional[str]
    email: Optional[str]
    password: Optional[str]
    create_date: Optional[str]
    community: Optional[str]
    phone: Optional[str]
    email_acceptance: Optional[int]
    message_acceptance: Optional[int]
    community: Optional[str]


    class Config:
        schema_extra = {
            "example": {
                "id": "1981904",
                "email": "john_doe@gmail.com",
                "password": "",
                "create_date": "19850109",
                "community": "USC00332098",
                "phone": "USC00332098",
                "email_acceptance": -11,
                "message_acceptance": -140,
                "status": "user",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}