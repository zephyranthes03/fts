
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.comment import (
    Comment_schema,
    Update_comment_schema,
)

# Retrieve all comments present in the database
async def retrieve_comments(mongodb_client: Optional[any], community_id: str, board_id: str,
                          page: int = 1, size: int = 10, search_keyword: str = "") -> list:
    database = mongodb_client[community_id]
    collection = database[f"comment_{board_id}"]

    comments = {}
    if search_keyword:
        comments = list(collection.find({},{
            { "content": {'$regex': f".*search_keyword.*", "$options" :"i"}}}
            ).skip((page - 1) * size).limit(size))
    else:
        comments = list(collection.find({}).skip((page - 1) * size).limit(size))
    return comments
                            

# Retrieve a comment with a matching station id
async def retrieve_comment_by_id(mongodb_client: Optional[any], community_id: str, board_id: str, id: str): # -> dict:
    database = mongodb_client[community_id]
    collection = database[f"comment_{board_id}"]

    comment = collection.find_one(
        {"_id": id}
    )
    return comment
    
# Add a new comment into to the database
async def add_comment(mongodb_client: Optional[any], community_id: str, board_id: str, comment_data: Comment_schema ) -> dict:
    database = mongodb_client[community_id]
    collection = database[f"comment_{board_id}"]

    new_comment = collection.insert_one(comment_data)
    created_comment = collection.find_one(
        {"_id": new_comment.inserted_id}
    )
    return created_comment


# Update a comment with a matching ID
async def update_comment(mongodb_client: Optional[any], community_id: str, board_id: str, id: str, comment_data: Update_comment_schema) -> dict:
    database = mongodb_client[community_id]
    collection = database[f"comment_{board_id}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": comment_data}
    )
    return update_result


# Delete a comment from the database
async def delete_comment(mongodb_client: Optional[any], community_id: str, board_id: str, id: str) -> int:
    database = mongodb_client[community_id]
    collection = database[f"comment_{board_id}"]

    delete_result = collection.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

