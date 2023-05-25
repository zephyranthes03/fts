import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/sampleimage'
DATABASE_HOST = os.getenv("DATABASE_HOST")
DIAG_DATABASE_NAME = os.getenv("DIAG_DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

#engine = sqlalchemy.create_engine(DATABASE_URL)
engine = sqlalchemy.create_engine(
        url="mysql+mysqldb://{0}:{1}@{2}/{3}".format(
            DATABASE_USERNAME, DATABASE_PASSWORD_UPDATED, DATABASE_HOST, DIAG_DATABASE_NAME
            )
        )

metadata = sqlalchemy.MetaData()

sampleimages = sqlalchemy.Table(
    DIAG_DATABASE_NAME,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
    sqlalchemy.Column("image_file", sqlalchemy.String(255), primary_key=True),
    sqlalchemy.Column("detail", sqlalchemy.Text),
    sqlalchemy.Column("inspection", sqlalchemy.Text),
    # sqlalchemy.Column("create_date", sqlalchemy.Date),
)

metadata.create_all(engine)

class SampleImage(BaseModel):
    __tablename__ = "SAMPLEIMAGE"
    id: str
    image_file: str
    detail: str
    inspection: str
    # create_date: datetime

# helpers

# crud operations



# Retrieve all sampleimages present in the database
async def retrieve_sampleimages() -> list:
    with engine.connect() as conn:        
        query = sampleimages.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a sampleimage with a matching station id
async def retrieve_sampleimage_by_id(id: str): # -> dict:
    with engine.connect() as conn:
        query = sampleimages.select().where(sampleimages.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new sampleimage into to the database
async def add_sampleimage(sampleimage_data: SampleImage) -> dict:
    with engine.connect() as conn:        
        query = sampleimages.insert().values(id=f"{sampleimage_data['id']}",image_file=f"{sampleimage_data['image_file']}",detail=f"{sampleimage_data['detail']}",
            inspection=sampleimage_data['inspection'])
        last_record_id = conn.execute(query)
        conn.commit()
        return {**sampleimage_data, "id": last_record_id}


# Update a sampleimage with a matching ID
async def update_sampleimage(id: str, sampleimage_data: SampleImage) -> dict:
    # Return false if an empty request body is sent.
    if len(sampleimage_data) < 1:
        return False
    with engine.connect() as conn:
        query = sampleimages.update().where(sampleimages.c.id==id).values(image_file=f"{sampleimage_data['image_file']}",detail=f"{sampleimage_data['detail']}",
            inspection=sampleimage_data['inspection'])   
        last_record_id = conn.execute(query)
        conn.commit()
        return {**sampleimage_data, "id": last_record_id}


# Delete a sampleimage from the database
async def delete_sampleimage(id: str):
    with engine.connect() as conn:        
        query = sampleimages.delete().where(sampleimages.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

