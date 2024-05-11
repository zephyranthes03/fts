
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.log_community import (
    log_community_schema,
    Update_log_community_schema,
)
from app.server.util.logging import logger

# Retrieve all Log_communities present in the database
# pagenation 

async def retrieve_Log_communities(mongodb_client: Optional[any], 
                          community_id: str, 
                          page: int = 1, size: int = 10, search_keyword: str = "") -> list:
    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    Log_communities = list(collection.find({}).skip((page - 1) * size).limit(size))
    return Log_communities

# Retrieve a log_community with a matching station id
async def retrieve_log_community_by_user_id(mongodb_client: Optional[any], 
                               community_id: str, user_id: str,
                               page: int = 1, size: int = 10) -> list: 
    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    Log_communities = list(collection.find({},{
        { "user_id": {user_id}}}
        ).skip((page - 1) * size).limit(size))

    return Log_communities

# Retrieve a log_community with a matching station id
async def retrieve_log_community_by_id(mongodb_client: Optional[any], 
                               community_id: str, id: str,
                               page: int = 1, size: int = 10) -> list: 
    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    Log_communities = list(collection.find({},{
        { "_id": {id}}}
        ).skip((page - 1) * size).limit(size))

    return Log_communities
    
# Add a new log_community into to the database
async def add_log_community(mongodb_client: Optional[any], 
                    community_id: str, user_id: str, log_community_data: log_community_schema ) -> dict:

    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    new_log_community = collection.insert_one(log_community_data)
    created_log_community = collection.find_one(
        {"_id": new_log_community.inserted_id}
    )
    return created_log_community


# Update a log_community with a matching ID
async def update_log_community(mongodb_client: Optional[any],
                       community_id: str, id: str, 
                       log_community_data: Update_log_community_schema) -> dict:

    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    update_result = collection.update_one(
        {"_id": id}, {"$set": log_community_data}
    )
    return update_result


# Delete a log_community from the database
async def delete_log_community(mongodb_client: Optional[any], 
                       community_id: str, user_id: str, id: str) -> int:

    collection_name = datetime.strftime(datetime.now(), '%Y-%m')  
    database = mongodb_client[f"log_{community_id}"]
    collection = database[collection_name]

    delete_result = collection.delete_one({"_id": id})
    # logger.info(delete_result)
    return delete_result

