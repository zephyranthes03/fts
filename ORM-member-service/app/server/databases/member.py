
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.member import (
    Member_schema,
    Update_member_schema,
)

# Retrieve all members present in the database
async def retrieve_members(mongodb_client: Optional[any], community_id: str) -> list:
    database = mongodb_client[f"community_member"]
    collection = database[f"member_{community_id}"]

    members = list(collection.find())
    return members


# Retrieve a member with a matching station id
async def retrieve_member_by_id(mongodb_client: Optional[any], community_id: str, id: str): # -> dict:
    database = mongodb_client[f"community_member"]
    collection = database[f"member_{community_id}"]

    member = collection.find_one(
        {"_id": id}
    )
    return member


# Retrieve a member with a matching station name
async def retrieve_member_by_name(mongodb_client: Optional[any], community_id: str, name: str): # -> dict:
    database = mongodb_client[f"community_member"]
    collection = database[f"member_{community_id}"]

    member = collection.find_one(
        {"name": name}
    )
    return member


# Add a new member into to the database
async def add_member(mongodb_client: Optional[any], community_id: str, member_data: Member_schema ) -> dict:

    database = mongodb_client[f"community_member"]
    collection = database[f"member_{community_id}"]

    new_member = collection.insert_one(member_data)
    created_member = collection.find_one(
        {"_id": new_member.inserted_id}
    )
    return created_member


# Update a member with a matching ID
async def update_member(mongodb_client: Optional[any], community_id: str, id: str, member_data: Update_member_schema) -> dict:
    database = mongodb_client[f"community_member"]
    collection = database[f"member_{community_id}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": member_data}
    )
    return update_result


# Delete a member from the database
async def delete_member(mongodb_client: Optional[any], community_id: str, id: str) -> int:
    database = mongodb_client[f"community_member"]
    collection = collection[f"member_{community_id}"]

    delete_result = collection.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

