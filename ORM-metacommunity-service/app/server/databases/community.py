
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.community import (
    Community_schema,
    Update_community_schema,
)

# Retrieve all communities present in the database
async def retrieve_communities(database: Optional[any]) -> list:
    communities = list(database.find())
    return communities


# Retrieve a community with a matching station id
async def retrieve_community_by_id(database: Optional[any], id: str): # -> dict:
    community = database.find_one(
        {"_id": id}
    )
    return community
    
# Add a new community into to the database
async def add_community(database: Optional[any], community_data: Community_schema ) -> dict:
    new_community = database.insert_one(community_data)
    created_community = database.find_one(
        {"_id": new_community.inserted_id}
    )
    return created_community


# Update a community with a matching ID
async def update_community(database: Optional[any], id: str, community_data: Update_community_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": community_data}
    )
    return update_result


# Delete a community from the database
async def delete_community(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

