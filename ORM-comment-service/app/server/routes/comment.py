from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.comment import (
    add_comment,
    delete_comment,
    update_comment,
    retrieve_comments,
    retrieve_comment_by_id,
    retrieve_comment_by_post_id,
)

from app.server.schemas.comment import (
    ErrorResponseModel,
    ResponseModel,
    Comment_schema,
    Update_comment_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}/{board_id}/{post_id}", response_description="Comment data added into the database")
async def add_comment_data(request: Request, community_id: str, board_id: str, post_id: str,
                           comment: Comment_schema = Body(...)):
    comment = jsonable_encoder(comment)
    new_comment = await add_comment(request.app.mongodb_client, 
                                    community_id, board_id, post_id, comment)
    return ResponseModel(new_comment, "Comment added successfully.")

@router.get("/{community_id}/{board_id}/{post_id}", response_description="Comments retrieved")
async def get_comments_data_post_id(request: Request, community_id: str, board_id: str, post_id:str, 
                          page: int = 1, size: int = 10, search_keyword: str = ""):
    comments = await retrieve_comment_by_post_id(request.app.mongodb_client, 
                                       community_id, board_id, post_id,
                                       page, size, search_keyword)
    comments_list = list()
    if comments:
        for comment in comments:
            # comment_dict = await comment_list_to_dict(comment)
            comments_list.append(comment)
        return comments_list

    return comments

@router.get("/{community_id}/{board_id}/{post_id}/id/{comment_id}", response_description="Comment data retrieved by comment_id")
async def get_comment_data_by_id(request: Request, community_id: str, board_id: str, post_id:str, comment_id: str, 
                          page: int = 1, size: int = 10, search_keyword: str = ""):
    comment = await retrieve_comment_by_id(request.app.mongodb_client, 
                                           community_id, board_id, post_id, comment_id,
                                           page, size, search_keyword)
    return comment

@router.put("/{community_id}/{board_id}/{post_id}/id/{comment_id}")
async def update_comment_data(request: Request, 
                              community_id: str, board_id: str, post_id:str, comment_id: str, 
                              req: Update_comment_schema = Body(...)):
    comment = {k: v for k, v in req.dict().items() if v is not None}

    if len(comment) >= 1:
        update_result = await update_comment(request.app.mongodb_client, 
                                             community_id, board_id, post_id, comment_id, comment)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Comment ID - {comment_id} not found"
            )

    if (
        existing_comment := await retrieve_comment_by_id(request.app.mongodb_client, 
                                                         community_id, board_id, post_id, comment_id)
    ) is not None:
        return ResponseModel(existing_comment, "Comment updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the comment data.",
    )


@router.delete("/{community_id}/{board_id}/{post_id}/id/{comment_id}")
async def delete_comment_data(request: Request, 
                              community_id: str, board_id: str, post_id:str, comment_id: str):
    deleted_comment = await delete_comment(request.app.mongodb_client, 
                                           community_id, board_id, post_id, comment_id)
    if deleted_comment:
        return ResponseModel(
            "Comment with ID: {} name delete is successful".format(comment_id),
            "Comment name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the comment data.",
    )

