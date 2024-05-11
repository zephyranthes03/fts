
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.diagnosis import (
    Diagnosis_schema,
    Update_diagnosis_schema,
)
from app.server.util.logging import logger

# Retrieve all diagnosises present in the database
async def retrieve_diagnosises(database: Optional[any]) -> list:
    diagnosises = list(database.find())
    return diagnosises


# Retrieve a diagnosis with a matching station id
async def retrieve_diagnosis_by_id(database: Optional[any], id: str): # -> dict:
    diagnosis = database.find_one(
        {"_id": id}
    )
    return diagnosis

# Retrieve a diagnosis with a matching station id
async def retrieve_diagnosis_by_name(database: Optional[any], name: str): # -> dict:
    diagnosis = database.find_one(
        {"diagnosis": name}
    )
    return diagnosis
    
# Add a new diagnosis into to the database
async def add_diagnosis(database: Optional[any], diagnosis_data: Diagnosis_schema ) -> dict:
    new_diagnosis = database.insert_one(diagnosis_data)
    created_diagnosis = database.find_one(
        {"_id": new_diagnosis.inserted_id}
    )
    return created_diagnosis


# Update a diagnosis with a matching ID
async def update_diagnosis(database: Optional[any], id: str, diagnosis_data: Update_diagnosis_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": diagnosis_data}
    )
    return update_result


# Delete a diagnosis from the database
async def delete_diagnosis(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    logger.info(delete_result)
    return delete_result

