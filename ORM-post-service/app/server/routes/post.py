from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.post import (
    add_post,
    delete_post,
    update_post,
    retrieve_posts,
    retrieve_post_by_id,
)

from app.server.schemas.post import (
    ErrorResponseModel,
    ResponseModel,
    Post_schema,
    Update_post_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}/{board_id}", response_description="Post data added into the database")
async def add_post_data(request: Request, community_id: str, board_id: str, post: Post_schema = Body(...)):
    post = jsonable_encoder(post)
    new_post = await add_post(request.app.mongodb_client,
                                community_id, board_id,
                                post)
    return ResponseModel(new_post, "Post added successfully.")

@router.get("/{community_id}/{board_id}", response_description="Posts retrieved")
async def get_posts_data(request: Request, community_id: str, board_id: str,
                          page: int = 1, size: int = 10, search_keyword: str = ""):
    posts = await retrieve_posts(request.app.mongodb_client,
                                   community_id, board_id,
                                   page, size, search_keyword)
    posts_list = list()
    if posts:
        for post in posts:
            # post_dict = await post_list_to_dict(post)
            posts_list.append(post)
        return posts_list

    return posts

@router.get("/{community_id}/{board_id}/{post_id}", response_description="Post data retrieved by post_id")
async def get_post_data(request: Request, community_id: str, board_id: str, post_id: str):
    post = await retrieve_post_by_id(request.app.mongodb_client,
                                       community_id, board_id,
                                       post_id)
    return post

@router.put("/{community_id}/{board_id}/{post_id}")
async def update_post_data(request: Request, community_id: str, board_id: str, post_id: str, req: Update_post_schema = Body(...)):
    post = {k: v for k, v in req.dict().items() if v is not None}

    if len(post) >= 1:
        update_result = await update_post(request.app.mongodb_client,
                                           community_id, board_id,
                                           post_id, post)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {post_id} not found"
            )

    if (
        existing_post := await retrieve_post_by_id(request.app.mongodb_client,
                                                     community_id, board_id, post_id)
    ) is not None:
        return ResponseModel(existing_post, "Post updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the post data.",
    )


@router.delete("/{community_id}/{board_id}/{post_id}")
async def delete_post_data(request: Request, community_id: str, board_id: str, post_id: str):
    deleted_post = await delete_post(request.app.mongodb_client,
                                       community_id, board_id,
                                       post_id)
    if deleted_post:
        return ResponseModel(
            "Post with ID: {} name delete is successful".format(post_id),
            "Post name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the post data.",
    )

