
from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.symptom_index import (
    Symptom_index_schema,
    Update_symptom_index_schema,
)

# Retrieve all symptom_indexes present in the database
async def retrieve_symptom_indexes(database: Optional[any]) -> list:
    symptom_indexes = list(database.find())
    return symptom_indexes


# Retrieve a symptom with a matching station id
async def retrieve_symptom_index_by_id(database: Optional[any], id: str): # -> dict:
    symptom = database.find_one(
        {"_id": id}
    )
    return symptom

# Retrieve a diagnosis with a matching name
async def retrieve_symptom_index_by_name(database: Optional[any], name: str): # -> dict:
    symptom = database.find_one(
        {"symptom": name}
    )
    return symptom
    
# Add a new symptom into to the database
async def add_symptom_index(database: Optional[any], symptom_index_data: Symptom_index_schema ) -> dict:
    new_symptom_index = database.insert_one(symptom_index_data)
    created_symptom_index = database.find_one(
        {"_id": new_symptom_index.inserted_id}
    )
    return created_symptom_index


# Update a symptom with a matching ID
async def update_symptom_index(database: Optional[any], id: str, symptom_index_data: Update_symptom_index_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": symptom_index_data}
    )
    return update_result


# Delete a symptom from the database
async def delete_symptom_index(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    return delete_result

