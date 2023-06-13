import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.database.common import SampleImage, database


#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/sampleimage'
DATABASE_HOST = os.getenv("DATABASE_HOST")
SYMPTOM_DATABASE_NAME = os.getenv("SYMPTOM_DATABASE_NAME")+"_image"
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

# Retrieve all sampleimages present in the database
async def retrieve_sampleimages() -> list:
    with database.engine.connect() as conn:        
        query = database.sampleimages.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list


# Retrieve a sampleimage with a matching station id
async def retrieve_sampleimage_by_id(id: str): # -> dict:
    with database.engine.connect() as conn:
        query = database.sampleimages.select().where(database.sampleimages.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new sampleimage into to the database
async def add_sampleimage(sampleimage_data: SampleImage) -> dict:
    with database.engine.connect() as conn:        
        query = database.sampleimages.insert().values(id=f"{sampleimage_data['id']}",symptom=f"{sampleimage_data['symptom']}",
                                                  area=f"{sampleimage_data['area']}",occur_pattern=f"{sampleimage_data['occur_pattern']}",
                                                  ages=f"{sampleimage_data['ages']}",sex=f"{sampleimage_data['sex']}",
                                                  bmi=f"{sampleimage_data['bmi']}",diagnosis=f"{sampleimage_data['diagnosis']}",
                                                  image_file=f"{sampleimage_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**sampleimage_data, "id": last_record_id}


# Update a sampleimage with a matching ID
async def update_sampleimage(id: str, sampleimage_data: SampleImage) -> dict:
    # Return false if an empty request body is sent.
    if len(sampleimage_data) < 1:
        return False
    with database.engine.connect() as conn:
        query = database.sampleimages.update().where(database.sampleimages.c.id==id).values(symptom=f"{sampleimage_data['symptom']}",
                                                                                    area=f"{sampleimage_data['area']}",
                                                                                    occur_pattern=f"{sampleimage_data['occur_pattern']}",
                                                                                    ages=f"{sampleimage_data['ages']}",
                                                                                    sex=f"{sampleimage_data['sex']}",
                                                                                    bmi=f"{sampleimage_data['bmi']}",
                                                                                    diagnosis=f"{sampleimage_data['diagnosis']}",
                                                                                    image_file=f"{sampleimage_data['image_file']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**sampleimage_data, "id": last_record_id}


# Delete a sampleimage from the database
async def delete_sampleimage(id: str):
    with database.engine.connect() as conn:        
        query = database.sampleimages.delete().where(database.sampleimages.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

