
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.post import (
    Post_schema,
    Update_post_schema,
)

# Retrieve all posts present in the database
# pagenation 

async def retrieve_posts(mongodb_client: Optional[any], 
                          community_id: str, post_id: str,
                          page: int = 1, size: int = 10, search_keyword: str = "") -> list:
    database = mongodb_client[f"post_{community_id}"]
    collection = database[f"post_{post_id}"]

    posts = {}
    if search_keyword:
        posts = list(collection.find({},{"$or":[
            { "title": {'$regex': f".*{search_keyword}.*", "$options" :"i"}},
            { "content": {'$regex': f".*{search_keyword}.*", "$options" :"i"}}]}
            ).skip((page - 1) * size).limit(size))
    else:
        posts = list(collection.find({}).skip((page - 1) * size).limit(size))
    return posts

# Retrieve a post with a matching station id
async def retrieve_post_by_id(mongodb_client: Optional[any], 
                               community_id: str, post_id: str, id: str): # -> dict:
    database = mongodb_client[f"post_{community_id}"]
    collection = database[f"post_{post_id}"]

    post = collection.find_one(
        {"_id": id}
    )
    return post
    
# Add a new post into to the database
async def add_post(mongodb_client: Optional[any], 
                    community_id: str, post_id: str, post_data: Post_schema ) -> dict:

    database = mongodb_client[f"post_{community_id}"]
    collection = database[f"post_{post_id}"]

    new_post = collection.insert_one(post_data)
    created_post = collection.find_one(
        {"_id": new_post.inserted_id}
    )
    return created_post


# Update a post with a matching ID
async def update_post(mongodb_client: Optional[any],
                       community_id: str, post_id: str, id: str, 
                       post_data: Update_post_schema) -> dict:

    database = mongodb_client[f"post_{community_id}"]
    collection = database[f"post_{post_id}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": post_data}
    )
    return update_result


# Delete a post from the database
async def delete_post(mongodb_client: Optional[any], 
                       community_id: str, post_id: str, id: str) -> int:

    database = mongodb_client[f"post_{community_id}"]
    collection = database[f"post_{post_id}"]

    delete_result = collection.delete_one({"_id": id})
    # print(delete_result,flush=True)
    return delete_result

