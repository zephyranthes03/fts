
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.comment import (
    Comment_schema,
    Update_comment_schema,
)

# Retrieve all comments present in the database
async def retrieve_comments(database: Optional[any]) -> list:
    comments = list(database.find())
    return comments


# Retrieve a comment with a matching station id
async def retrieve_comment_by_id(database: Optional[any], id: str): # -> dict:
    comment = database.find_one(
        {"_id": id}
    )
    return comment
    
# Add a new comment into to the database
async def add_comment(database: Optional[any], comment_data: Comment_schema ) -> dict:
    new_comment = database.insert_one(comment_data)
    created_comment = database.find_one(
        {"_id": new_comment.inserted_id}
    )
    return created_comment


# Update a comment with a matching ID
async def update_comment(database: Optional[any], id: str, comment_data: Update_comment_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": comment_data}
    )
    return update_result


# Delete a comment from the database
async def delete_comment(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

