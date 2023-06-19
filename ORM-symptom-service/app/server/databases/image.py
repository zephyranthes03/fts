import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


from app.server.schemas.images import (
    SampleImageSchema,
    UpdateSampleImageModel,
)

# Retrieve all sampleImages present in the database
async def retrieve_sampleimages(database: Optional[any]) -> list:
    sampleImages = list(database.find())
    return sampleImages


# Retrieve a sampleImage with a matching station id
async def retrieve_sampleimage_by_id(database: Optional[any], id: str): # -> dict:
    sampleImage = database.find_one(
        {"_id": id}
    )
    return sampleImage
    
# Add a new sampleImage into to the database
async def add_sampleimage(database: Optional[any], sampleImage_data: SampleImageSchema ) -> dict:
    new_sampleImage = database.insert_one(sampleImage_data)
    created_sampleImage = database.find_one(
        {"_id": new_sampleImage.inserted_id}
    )
    return created_sampleImage


# Update a sampleImage with a matching ID
async def update_sampleimage(database: Optional[any], id: str, sampleImage_data: UpdateSampleImageModel) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": sampleImage_data}
    )
    return update_result


# Delete a sampleImage from the database
async def delete_sampleimage(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

