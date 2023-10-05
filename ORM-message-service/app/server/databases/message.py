
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI
from app.config.config import settings

from app.server.schemas.message import (
    Message_schema,
    Update_message_schema,
)

# Retrieve all messages present in the database
# pagenation 

async def retrieve_messages(mongodb_client: Optional[any], 
                          receiver: str, message: str,
                          page: int = 1, size: int = 10) -> list:
    database = mongodb_client[settings.DATABASE_MESSAGE]
    collection = database[f"message_{str(hash(receiver)%100)}"]

    messages = []
    if message:
        messages = list(collection.find({},{"$and":[
            { "receiver": {receiver}},
            { "message": {message}}]}
            ).skip((page - 1) * size).limit(size))
    else:
        messages = list(collection.find({},{
            { "receiver": {receiver}}}
            ).skip((page - 1) * size).limit(size))
    return messages

# Retrieve a message with a matching station id
async def retrieve_message_by_id(mongodb_client: Optional[any], 
                               user_id: str, id: str): # -> dict:
    database = mongodb_client[settings.DATABASE_MESSAGE]
    collection = database[f"message_{str(hash(user_id)%100)}"]

    message = collection.find_one(
        {"_id": id}
    )
    return message
    
# Add a new message into to the database
async def add_message(mongodb_client: Optional[any], 
                    user_id: str, message_data: Message_schema ) -> dict:

    database = mongodb_client[settings.DATABASE_MESSAGE]
    collection = database[f"message_{str(hash(user_id)%100)}"]

    new_message = collection.insert_one(message_data)
    created_message = collection.find_one(
        {"_id": new_message.id}
    )
    return created_message


# Update a message with a matching ID
async def update_message(mongodb_client: Optional[any],
                       user_id: str, id: str, 
                       message_data: Update_message_schema) -> dict:

    database = mongodb_client[settings.DATABASE_MESSAGE]
    collection = database[f"message_{str(hash(user_id)%100)}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": message_data}
    )
    return update_result


# Delete a message from the database
async def delete_message(mongodb_client: Optional[any], 
                       user_id: str, id: str) -> int:

    database = mongodb_client[settings.DATABASE_MESSAGE]
    collection = database[f"message_{str(hash(user_id)%100)}"]

    delete_result = collection.delete_one({"_id": id})
    # print(delete_result,flush=True)
    return delete_result

