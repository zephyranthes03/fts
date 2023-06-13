import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.database.common import Disease, database


#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/disease'
DATABASE_HOST = os.getenv("DATABASE_HOST")
SYMPTOM_DATABASE_NAME = os.getenv("SYMPTOM_DATABASE_NAME")+ "_disease"
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DISEASE_TABLENAME = "disease"

# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)


# Retrieve all diseases present in the database
async def retrieve_diseases() -> list:
    with database.engine.connect() as conn:        
        query = database.diseases.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a disease with a matching station id
async def retrieve_disease_by_id(id: str): # -> dict:
    with database.engine.connect() as conn:
        query = database.diseases.select().where(database.diseases.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new disease into to the database
async def add_disease(disease_data: Disease) -> dict:
    with database.engine.connect() as conn:        
        query = database.diseases.insert().values(id=f"{disease_data['id']}",symptom=f"{disease_data['symptom']}",
                                                  area=f"{disease_data['area']}",occur_pattern=f"{disease_data['occur_pattern']}",
                                                  ages=f"{disease_data['ages']}",sex=f"{disease_data['sex']}",
                                                  diagnosis=f"{disease_data['diagnosis']}",image_file=f"{disease_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**disease_data, "id": last_record_id}


# Update a disease with a matching ID
async def update_disease(id: str, disease_data: Disease) -> dict:
    # Return false if an empty request body is sent.
    if len(disease_data) < 1:
        return False
    with database.engine.connect() as conn:
        query = database.diseases.update().where(database.diseases.c.id==id).values(symptom=f"{disease_data['symptom']}",
                                                                                    area=f"{disease_data['area']}",
                                                                                    occur_pattern=f"{disease_data['occur_pattern']}",
                                                                                    ages=f"{disease_data['ages']}",
                                                                                    detsexail=f"{disease_data['sex']}",
                                                                                    diagnosis=f"{disease_data['diagnosis']}",
                                                                                    image_file=f"{disease_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**disease_data, "id": last_record_id}


# Delete a disease from the database
async def delete_disease(id: str):
    with database.engine.connect() as conn:        
        query = database.diseases.delete().where(database.diseases.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

