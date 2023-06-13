import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.database.common import Symptom, database


# Retrieve all symptoms present in the database
async def retrieve_symptoms() -> list:
    with database.engine.connect() as conn:        
        query = database.symptoms.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list

# Retrieve a symptom with a matching station id
async def retrieve_symptom_by_id(id: str): # -> dict:
    with database.engine.connect() as conn:
        query = database.symptoms.select().where(database.symptoms.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new symptom into to the database
async def add_symptom(symptom_data: Symptom) -> dict:
    with database.engine.connect() as conn:        
        query = database.symptoms.insert().values(id=f"{symptom_data['id']}",symptom=f"{symptom_data['symptom']}",
                                                  area=f"{symptom_data['area']}",occur_pattern=f"{symptom_data['occur_pattern']}",
                                                  ages=f"{symptom_data['ages']}",sex=f"{symptom_data['sex']}",
                                                  bmi=f"{symptom_data['bmi']}",diagnosis=f"{symptom_data['diagnosis']}",
                                                  image_file=f"{symptom_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**symptom_data, "id": last_record_id}


# Update a symptom with a matching ID
async def update_symptom(id: str, symptom_data: Symptom) -> dict:
    # Return false if an empty request body is sent.
    if len(symptom_data) < 1:
        return False
    with database.engine.connect() as conn:
        query = database.symptoms.update().where(database.symptoms.c.id==id).values(symptom=f"{symptom_data['symptom']}",
                                                                                    area=f"{symptom_data['area']}",
                                                                                    occur_pattern=f"{symptom_data['occur_pattern']}",
                                                                                    ages=f"{symptom_data['ages']}",
                                                                                    sex=f"{symptom_data['sex']}",
                                                                                    bmi=f"{symptom_data['bmi']}",
                                                                                    diagnosis=f"{symptom_data['diagnosis']}",
                                                                                    image_file=f"{symptom_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**symptom_data, "id": last_record_id}


# Delete a symptom from the database
async def delete_symptom(id: str):
    with database.engine.connect() as conn:        
        query = database.symptoms.delete().where(database.symptoms.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

