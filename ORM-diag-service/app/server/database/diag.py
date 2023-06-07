import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.database.common import Diag, database

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/diag'
DATABASE_HOST = os.getenv("DATABASE_HOST")
DIAG_DATABASE_NAME = os.getenv("DIAG_DATABASE_NAME")
DIAG_DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DIAG_TABLENAME = "diag"

# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)



# Retrieve all diags present in the database
async def retrieve_diags() -> list:
    with database.engine.connect() as conn:        
        query = database.diags.select()
        result_list = list()
        for row in conn.execute(query):
            result_list.append(list(row))
        return result_list

# Retrieve a diag with a matching station id
async def retrieve_diag_by_id(id: str): # -> dict:
    with database.engine.connect() as conn:
        query = database.diags.select().where(database.diags.c.id==id)
        result = list()
        for row in conn.execute(query):
            result = list(row)
        return result

# Add a new diag into to the database
async def add_diag(diag_data: Diag) -> dict:
    with database.engine.connect() as conn:        
        query = database.diags.insert().values(id=f"{diag_data['id']}",disease=f"{diag_data['disease']}",image_file=f"{diag_data['image_file']}",
                                      detail=f"{diag_data['detail']}", queationaire=f"{diag_data['queationaire']}")
        last_record_id = conn.execute(query)
        conn.commit()
        return {**diag_data, "id": last_record_id}


# Update a diag with a matching ID
async def update_diag(id: str, diag_data: Diag) -> dict:
    # Return false if an empty request body is sent.
    if len(diag_data) < 1:
        return False
    with database.engine.connect() as conn:
        query = database.diags.update().where(database.diags.c.id==id).values(disease=f"{diag_data['disease']}",image_file=f"{diag_data['image_file']}",
                                                            detail=f"{diag_data['detail']}", queationaire=f"{diag_data['queationaire']}")   
        last_record_id = conn.execute(query)
        conn.commit()
        return {**diag_data, "id": last_record_id}


# Delete a diag from the database
async def delete_diag(id: str):
    with database.engine.connect() as conn:        
        query = database.diags.delete().where(database.diags.c.id==id)
        conn.execute(query)
        conn.commit()
        return True
    return False

