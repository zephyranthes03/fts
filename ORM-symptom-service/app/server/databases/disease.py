import sqlalchemy
import urllib
import os

from datetime import datetime
from sqlalchemy.orm import Session

from typing import List, Optional

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.server.schemas.disease import (
    DiseaseSchema,
    UpdateDiseaseModel,
)

# Retrieve all diseases present in the database
async def retrieve_diseases(database: Optional[any]) -> list:
    diseases = list(database.find())
    return diseases


# Retrieve a disease with a matching station id
async def retrieve_disease_by_id(database: Optional[any], id: str): # -> dict:
    disease = database.find_one(
        {"_id": id}
    )
    return disease
    
# Add a new disease into to the database
async def add_disease(database: Optional[any], disease_data: DiseaseSchema ) -> dict:
    new_disease = database.insert_one(disease_data)
    created_disease = database.find_one(
        {"_id": new_disease.inserted_id}
    )
    return created_disease


# Update a disease with a matching ID
async def update_disease(database: Optional[any], id: str, disease_data: UpdateDiseaseModel) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": disease_data}
    )
    return update_result


# Delete a disease from the database
async def delete_disease(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

