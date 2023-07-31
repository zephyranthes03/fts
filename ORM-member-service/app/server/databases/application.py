
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.application import (
    Application_schema,
    Update_application_schema,
)

# Retrieve all applications present in the database
async def retrieve_applications(database: Optional[any]) -> list:
    applications = list(database.find())
    return applications


# Retrieve a application with a matching station id
async def retrieve_application_by_id(database: Optional[any], id: str): # -> dict:
    application = database.find_one(
        {"_id": id}
    )
    return application


# Retrieve a application with a matching station name
async def retrieve_application_by_name(database: Optional[any], name: str): # -> dict:
    application = database.find_one(
        {"name": name}
    )
    return application


# Add a new application into to the database
async def add_application(database: Optional[any], application_data: Application_schema ) -> dict:
    new_application = database.insert_one(application_data)
    created_application = database.find_one(
        {"_id": new_application.inserted_id}
    )
    return created_application


# Update a application with a matching ID
async def update_application(database: Optional[any], id: str, application_data: Update_application_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": application_data}
    )
    return update_result


# Delete a application from the database
async def delete_application(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

