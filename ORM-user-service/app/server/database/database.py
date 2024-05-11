import sqlalchemy
from sqlalchemy_utils import database_exists

import urllib
import os


from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.util.encrypt import (
    set_password,
    check_password_hash
)
from app.server.util.logging import logger

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/user'
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("USER_DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

#engine = sqlalchemy.create_engine(DATABASE_URL)
db_url="mysql+mysqldb://{0}:{1}@{2}/{3}".format(
    DATABASE_USERNAME, DATABASE_PASSWORD_UPDATED, DATABASE_HOST, DATABASE_NAME
    )

engine = sqlalchemy.create_engine(db_url)
if not database_exists(engine.url):
    sqlalchemy.create_database(engine.url)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    DATABASE_NAME,
    metadata,
    # sqlalchemy.Column("id", sqlalchemy.String(64), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(64), primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("create_date", sqlalchemy.DateTime),
    sqlalchemy.Column("community", sqlalchemy.Text),
    sqlalchemy.Column("phone", sqlalchemy.String(15)),
    sqlalchemy.Column("email_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("message_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("user_type", sqlalchemy.String(255)),
    sqlalchemy.Column("account_type", sqlalchemy.String(255)),
    sqlalchemy.Column("expire_time", sqlalchemy.Integer),
    sqlalchemy.Column("last_check_time", sqlalchemy.Text),
    sqlalchemy.Column("interested_tag", sqlalchemy.Text),
    sqlalchemy.Column("message", sqlalchemy.Boolean),
    sqlalchemy.Column("friend", sqlalchemy.Text),
    sqlalchemy.Column("permission", sqlalchemy.Text),
    sqlalchemy.Column("symptom_id", sqlalchemy.String(1024)),
    sqlalchemy.Column("symptom_tag", sqlalchemy.String(1024)),
    sqlalchemy.Column("username", sqlalchemy.String(64)),
    sqlalchemy.Column("nickname", sqlalchemy.String(64)),
    sqlalchemy.Column("age", sqlalchemy.String(8)),
    sqlalchemy.Column("gender", sqlalchemy.String(16))
    # sqlalchemy.Column("date_convert", sqlalchemy.Date),
)

metadata.create_all(engine)

class User(BaseModel):
    __tablename__ = DATABASE_NAME
    # id: str
    email: str
    password: str
    create_date: datetime
    community: str
    phone: str
    email_acceptance: str
    message_acceptance: str
    user_type: str
    account_type: str
    expire_time: int
    last_check_time: str
    interested_tag: str
    message: bool
    friend: str
    permission: str
    symptom_id: str
    symptom_tag: str
    username: str
    nickname: str
    age: str
    gender: str
    

class socialEmailSignup(BaseModel):
    email: str
    login_type: str
    extra_data: str
    access_token: str
    refresh_token: str

class SocialEmailLogin(BaseModel):
    email: str
    login_type: str
    access_token: str
    refresh_token: str

class Email(BaseModel):
    email: str
    password: str

# helpers

# crud operations




# Retrieve all users present in the database
async def retrieve_users() -> list:
    with engine.connect() as conn:        
        query = users.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a user with a matching station id
async def retrieve_user_by_id(user_id: str): # -> dict:
    with engine.connect() as conn:
        query = users.select().where(users.c.id==user_id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result
    
# Retrieve a user with a matching station id
async def retrieve_user_by_email(email: str): # -> dict:
    with engine.connect() as conn:
        query = users.select().where(users.c.email==email)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        # logger.info(result)
        return result

# Retrieve a user with a matching social_email
async def retrieve_user_by_social_email(socialEmail: SocialEmailLogin): # -> dict:    
    with engine.connect() as conn:
        query = users.select().where(users.c.email==socialEmail['email']).filter(users.c.account_type.contains(socialEmail['login_type']))
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result
    
async def retrieve_user_by_social_email(socialEmail: socialEmailSignup): # -> dict:    
    with engine.connect() as conn:
        query = users.select().where(users.c.email==socialEmail['email']).filter(users.c.account_type.contains(socialEmail['login_type']))
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Retrieve a user with a matching email password
async def retrieve_user_by_email_password(email: Email): # -> dict:
    with engine.connect() as conn:
        ## TODO: password comparing debugging!!
        query = users.select().where(users.c.email==email['email']).where(users.c.password==email['password'])
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result


# Add a new user into to the database
async def add_users(user_data: List[User]) -> dict:
    count = 0
    count_exist = 0
    with engine.connect() as conn:
        for user in user_data:
            exist_field = await retrieve_user_by_email(user_data['email'])
            if exist_field:
                count_exist += 1
            else:
                count += 1
            
                query = users.insert().values(email=f"{user['email']}",password=f"{user['password']}",
                    create_date=user['create_date'],community=user['community'],phone=user['phone'],
                    email_acceptance=user['email_acceptance'], message_acceptance=user['message_acceptance'], 
                    user_type=user['user_type'],account_type=user['account_type'],expire_time=user['expire_time'],
                    last_check_time=user['last_check_time'],interested_tag=user['interested_tag'],
                    message=user['message'],friend=user['friend'],permission=user['permission'],
                    symptom_id=user_data['symptom_id'],symptom_tag=user_data['symptom_tag'],
                    username=user_data['username'],nickname=user_data['nickname'],age=user_data['age'],
                    gender=user_data['gender'])
                last_record_id = conn.execute(query)
            conn.commit()
        return {"Total inserted record": count, "Total exist record": count_exist}



# Add a new user into to the database
async def add_social_user(user_data: User) -> dict:
    with engine.connect() as conn:
        exist_field = await retrieve_user_by_social_email(user_data)
        if exist_field:
            return {"message": "user already exist"}
        
        query = users.insert().values(email=f"{user_data['email']}",password=f"{user_data['password']}",
                create_date=user_data['create_date'],community=user_data['community'],phone=user_data['phone'],
                email_acceptance=user_data['email_acceptance'], message_acceptance=user_data['message_acceptance'], 
                user_type=user_data['user_type'],account_type=user_data['account_type'],expire_time=user_data['expire_time'],
                last_check_time=user_data['last_check_time'],interested_tag=user_data['interested_tag'],
                message=user_data['message'],friend=user_data['friend'],permission=user_data['permission'],
                symptom_id=user_data['symptom_id'],symptom_tag=user_data['symptom_tag'],username=user_data['username'],
                nickname=user_data['nickname'],age=user_data['age'],gender=user_data['gender'])
        last_record_id = conn.execute(query)
        conn.commit()
        return {**user_data, "email": last_record_id}
    
# Add a new user into to the database
async def add_user(user_data: User) -> dict:
    with engine.connect() as conn:
        exist_field = await retrieve_user_by_email(user_data['email'])
        if exist_field:
            return {"message": "user already exist"}
        
        query = users.insert().values(email=f"{user_data['email']}",password=f"{user_data['password']}",
                create_date=user_data['create_date'],community=user_data['community'],phone=user_data['phone'],
                email_acceptance=user_data['email_acceptance'], message_acceptance=user_data['message_acceptance'], 
                user_type=user_data['user_type'],account_type=user_data['account_type'],expire_time=user_data['expire_time'],
                last_check_time=user_data['last_check_time'],interested_tag=user_data['interested_tag'],
                message=user_data['message'],friend=user_data['friend'],permission=user_data['permission'],
                symptom_id=user_data['symptom_id'],symptom_tag=user_data['symptom_tag'],username=user_data['username'],
                nickname=user_data['nickname'],age=user_data['age'],gender=user_data['gender'])
        last_record_id = conn.execute(query)
        conn.commit()
        return {**user_data, "email": last_record_id}


# Update a user with a matching ID
async def update_user(user_email: str, user_data: User) -> dict:
    # Return false if an empty request body is sent.
    if len(user_data) < 1:
        return False
    with engine.connect() as conn:
        query = users.update().where(users.c.email==user_email).values(password=f"{user_data['password']}",
            create_date=user_data['create_date'],community=user_data['community'],phone=user_data['phone'],
            email_acceptance=user_data['email_acceptance'], message_acceptance=user_data['message_acceptance'], 
            user_type=user_data['user_type'],account_type=user_data['account_type'],expire_time=user_data['expire_time'],
            last_check_time=user_data['last_check_time'],interested_tag=user_data['interested_tag'],message=user_data['message'],
            friend=user_data['friend'],permission=user_data['permission'],symptom_id=user_data['symptom_id'],
            symptom_tag=user_data['symptom_tag'],username=user_data['username'],nickname=user_data['nickname'],age=user_data['age'],
            gender=user_data['gender'])
        last_record_id = conn.execute(query)

        conn.commit()
        return {**user_data, "email": last_record_id}


# Delete a user from the database
async def delete_user(user_email: str):
    with engine.connect() as conn:        
        query = users.delete().where(users.c.email==user_email)
        conn.execute(query)
        conn.commit()
        return True
    return False

