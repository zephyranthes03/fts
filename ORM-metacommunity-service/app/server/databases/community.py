
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.config.config import settings

from app.server.schemas.community import (
    Community_schema,
    Update_community_schema,
)

# Retrieve all communities present in the database
async def retrieve_communities(mongodb_client: Optional[any]) -> list:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]

    communities = list(collection.find())
    return communities


# Retrieve a community with a matching station id
async def retrieve_community_by_id(mongodb_client: Optional[any], id: str): # -> dict:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]

    community = collection.find_one(
        {"_id": id}
    )
    return community

# Retrieve a community with a matching station id
async def retrieve_community_by_name(mongodb_client: Optional[any], name: str): # -> dict:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]
    community = collection.find_one(
        {"name": name}
    )
    return community


# Add a new community into to the database
async def add_community(mongodb_client: Optional[any], community_data: Community_schema ) -> dict:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]
    new_community = collection.insert_one(community_data)
    created_community = collection.find_one(
        {"_id": new_community.inserted_id}
    )
    return created_community


# Update a community with a matching ID
async def update_community(mongodb_client: Optional[any], id: str, community_data: Update_community_schema) -> dict:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]
    update_result = collection.update_one(
        {"_id": id}, {"$set": community_data}
    )

    return update_result


# Delete a community from the database
async def delete_community(mongodb_client: Optional[any], id: str) -> int:
    database = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection = database[settings.DATABASE_METACOMMUNITY]
    delete_result = collection.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

