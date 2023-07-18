
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.member import (
    Member_schema,
    Update_member_schema,
)

# Retrieve all members present in the database
async def retrieve_members(database: Optional[any]) -> list:
    members = list(database.find())
    return members


# Retrieve a member with a matching station id
async def retrieve_member_by_id(database: Optional[any], id: str): # -> dict:
    member = database.find_one(
        {"_id": id}
    )
    return member


# Retrieve a member with a matching station name
async def retrieve_member_by_name(database: Optional[any], name: str): # -> dict:
    member = database.find_one(
        {"name": name}
    )
    return member


# Add a new member into to the database
async def add_member(database: Optional[any], member_data: Member_schema ) -> dict:
    new_member = database.insert_one(member_data)
    created_member = database.find_one(
        {"_id": new_member.inserted_id}
    )
    return created_member


# Update a member with a matching ID
async def update_member(database: Optional[any], id: str, member_data: Update_member_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": member_data}
    )
    return update_result


# Delete a member from the database
async def delete_member(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

