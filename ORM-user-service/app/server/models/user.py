from typing import Optional

from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    # id: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    create_date: str = Field(...)
    community: str = Field(...)
    phone: str = Field(...)
    email_acceptance: str = Field(...)
    message_acceptance: str = Field(...)
    user_type: str = Field(...) # user, provider, admin
    expire_time: int = Field(...)
    last_check_time: str = Field(...) # 커뮤니티별 마지막 확인 시간 - 나중에 마지막 확인 시간 이후에 등록된 글에 추가 태그(new)를 출력하기 위해 사용
    interested_tag: str = Field(...)
    message: bool = Field(...)
    friend: str = Field(...)
    permission: str = Field(...) # all|close|friend|community 

    class Config:
        schema_extra = {
            "example": {
                "email": "john_doe1@gmail.com",
                "password": "test",
                "create_date": "2021-01-01 00:00:00",
                "community": {'acne':{'grade':'user','status':'early'}},
                "phone": "72065122567",
                "email_acceptance": "all",
                "message_acceptance": ['community','system'],
                "user_type": "user",
                "expire_time": 30,
                "last_check_time": {'community_id':'2021-01-01T00:00:00Z'},
                "interested_tag": ['tag1', 'tag2'],
                "message": False,
                "friend": [],
                "permission": {'survey':'open'}

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
    # email: Optional[str]
    password: Optional[str]
    create_date: Optional[str]
    community: Optional[str] # Optional[dict]
    phone: Optional[str]
    email_acceptance: Optional[str]
    message_acceptance: Optional[str] # Optional[list]
    user_type: Optional[str]
    expire_time: Optional[int]
    last_check_time: Optional[str] # Optional[dict] # 커뮤니티별 마지막 확인 시간 - 나중에 마지막 확인 시간 이후에 등록된 글에 추가 태그(new)를 출력하기 위해 사용
    interested_tag: Optional[str] # Optional[list]
    message: Optional[bool]
    friend: Optional[str] # Optional[list]
    permission: Optional[str] # Optional[dict] # all|close|friend|community ?

    class Config:
        schema_extra = {
            "example": {
                # "email": "john_doe@gmail.com",
                "password": "test",
                "create_date": "2021-01-01 00:00:00",
                "community": {'acne':{'grade':'user','status':'early'}},
                "phone": "72065122567",
                "email_acceptance": "all",
                "message_acceptance": ['community','system'],
                "user_type": "user",
                "expire_time": 30,
                "last_check_time": {'community_id':'2021-01-01T00:00:00Z'},
                "interested_tag": ['tag1', 'tag2'],
                "message": False,
                "friend": [],
                "permission": {'survey':'open'}
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