import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/diag'
DATABASE_HOST = os.getenv("DATABASE_HOST")
DIAG_DATABASE_NAME = os.getenv("DIAG_DATABASE_NAME")
DIAG_DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DIAG_TABLENAME = "SAMPLEIMAGE"

# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

#engine = sqlalchemy.create_engine(DATABASE_URL)
engine = sqlalchemy.create_engine(
        url="mysql+mysqldb://{0}:{1}@{2}/{3}".format(
            DIAG_DATABASE_USERNAME, DATABASE_PASSWORD_UPDATED, DATABASE_HOST, DIAG_DATABASE_NAME
            )
        )

metadata = sqlalchemy.MetaData()

diags = sqlalchemy.Table(
    DIAG_TABLENAME,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String(45)),
    sqlalchemy.Column("image_file", sqlalchemy.Text),
    sqlalchemy.Column("disease", sqlalchemy.String(255), primary_key=True),
    # sqlalchemy.Column("create_date", sqlalchemy.Date),
)

metadata.create_all(engine)

class Diag(BaseModel):
    __tablename__ = DIAG_TABLENAME
    id: str
    user_id: str
    image_file: str
    disease: str
    # create_date: datetime

# helpers

# crud operations



# Retrieve all diags present in the database
async def retrieve_diags() -> list:
    with engine.connect() as conn:        
        query = diags.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a diag with a matching station id
async def retrieve_diag_by_id(id: str): # -> dict:
    with engine.connect() as conn:
        query = diags.select().where(diags.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new diag into to the database
async def add_diag(diag_data: Diag) -> dict:
    with engine.connect() as conn:        
        query = diags.insert().values(id=f"{diag_data['id']}",user_id=f"{diag_data['user_id']}",image_file=f"{diag_data['image_file']}",disease=f"{diag_data['disease']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**diag_data, "id": last_record_id}


# Update a diag with a matching ID
async def update_diag(id: str, diag_data: Diag) -> dict:
    # Return false if an empty request body is sent.
    if len(diag_data) < 1:
        return False
    with engine.connect() as conn:
        query = diags.update().where(diags.c.id==id).values(user_id=f"{diag_data['user_id']}",image_file=f"{diag_data['image_file']}",disease=f"{diag_data['disease']}")   
        last_record_id = conn.execute(query)
        conn.commit()
        return {**diag_data, "id": last_record_id}


# Delete a diag from the database
async def delete_diag(id: str):
    with engine.connect() as conn:        
        query = diags.delete().where(diags.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

