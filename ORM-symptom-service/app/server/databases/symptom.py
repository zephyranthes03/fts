import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel


from app.server.schemas.symptom import (
    SymptomSchema,
    UpdateSymptomModel,
)

# Retrieve all symptoms present in the database
async def retrieve_symptoms(database: Optional[any]) -> list:
    symptoms = list(database.find())
    return symptoms


# Retrieve a symptom with a matching station id
async def retrieve_symptom_by_id(database: Optional[any], id: str): # -> dict:
    symptom = database.find_one(
        {"_id": id}
    )
    return symptom
    
# Add a new symptom into to the database
async def add_symptom(database: Optional[any], symptom_data: SymptomSchema ) -> dict:
    new_symptom = database.insert_one(symptom_data)
    created_symptom = database.find_one(
        {"_id": new_symptom.inserted_id}
    )
    return created_symptom


# Update a symptom with a matching ID
async def update_symptom(database: Optional[any], id: str, symptom_data: UpdateSymptomModel) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": symptom_data}
    )
    return update_result


# Delete a symptom from the database
async def delete_symptom(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

