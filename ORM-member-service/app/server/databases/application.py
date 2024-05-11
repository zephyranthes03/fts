
from datetime import datetime

from typing import List, Optional
from app.server.util.logging import logger

# import databases
# from fastapi import FastAPI
from app.config.config import settings
from app.server.schemas.application import (
    Application_schema,
    Update_application_schema,
)

# Retrieve all applications present in the database
async def retrieve_applications(mongodb_client: Optional[any], community_id: str) -> list:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    applications = list(collection.find())
    return applications


# Retrieve a application with a matching station id
async def retrieve_application_by_id(mongodb_client: Optional[any], community_id: str, id: str): # -> dict:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    application = collection.find_one(
        {"_id": id}
    )
    return application


# Retrieve a application with a matching station name
async def retrieve_application_by_name(mongodb_client: Optional[any], community_id: str, name: str): # -> dict:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    application = collection.find_one(
        {"name": name}
    )
    return application


# Add a new application into to the database
async def add_application(mongodb_client: Optional[any], community_id: str, application_data: Application_schema ) -> dict:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    new_application = collection.insert_one(application_data)
    created_application = collection.find_one(
        {"_id": new_application.inserted_id}
    )
    return created_application


# Update a application with a matching ID
async def update_application(mongodb_client: Optional[any], community_id: str, id: str, application_data: Update_application_schema) -> dict:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": application_data}
    )
    return update_result


# Delete a application from the database
async def delete_application(mongodb_client: Optional[any], community_id: str, id: str) -> int:
    database = mongodb_client[settings.DATABASE_APPLICATION]
    collection = database[f"application_{community_id}"]

    delete_result = collection.delete_one({"_id": id})
    logger.info(delete_result)
    return delete_result

