import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/disease'
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

diseases = sqlalchemy.Table(
    DIAG_DATABASE_NAME,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
    sqlalchemy.Column("disease", sqlalchemy.String(255), primary_key=True),
    sqlalchemy.Column("detail", sqlalchemy.Text),
    sqlalchemy.Column("queationaire", sqlalchemy.Text),
    # sqlalchemy.Column("create_date", sqlalchemy.Date),
)

metadata.create_all(engine)

class Disease(BaseModel):
    __tablename__ = DIAG_DATABASE_NAME
    id: str
    disease: str
    detail: str
    queationaire: str
    # create_date: datetime

# helpers

# crud operations



# Retrieve all diseases present in the database
async def retrieve_diseases() -> list:
    with engine.connect() as conn:        
        query = diseases.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a disease with a matching station id
async def retrieve_disease_by_id(id: str): # -> dict:
    with engine.connect() as conn:
        query = diseases.select().where(diseases.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new disease into to the database
async def add_disease(disease_data: Disease) -> dict:
    with engine.connect() as conn:        
        query = diseases.insert().values(id=f"{disease_data['id']}",disease=f"{disease_data['disease']}",detail=f"{disease_data['detail']}",
            queationaire=disease_data['queationaire'])
        last_record_id = conn.execute(query)
        conn.commit()
        return {**disease_data, "id": last_record_id}


# Update a disease with a matching ID
async def update_disease(id: str, disease_data: Disease) -> dict:
    # Return false if an empty request body is sent.
    if len(disease_data) < 1:
        return False
    with engine.connect() as conn:
        query = diseases.update().where(diseases.c.id==id).values(disease=f"{disease_data['disease']}",detail=f"{disease_data['detail']}",
            queationaire=disease_data['queationaire'])   
        last_record_id = conn.execute(query)
        conn.commit()
        return {**disease_data, "id": last_record_id}


# Delete a disease from the database
async def delete_disease(id: str):
    with engine.connect() as conn:        
        query = diseases.delete().where(diseases.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

