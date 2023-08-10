import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

# templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.comment import (
    read_comment_by_id,
    read_comment_by_name,
    read_comments,
    add_comment,
    delete_comment,
    update_comment,
)

from app.server.schemas.comment import (
    ErrorResponseModel,
    ResponseModel,
    Comment_schema,
    Update_comment_schema
)


router = APIRouter()



@router.post("/{community_id}/{board_id}/post/{post_id}", response_description="Comment data folder added into the database")
async def add_comment_data(community_id:str, board_id:str, post_id:str, comment: Comment_schema = Body(...), dependencies:dict=Depends(verify_token)):
    comment = jsonable_encoder(comment)
    new_comment = await add_comment(community_id, board_id, post_id, comment)
    if new_comment.get('error', None):
        return ErrorResponseModel(
            new_comment.get('error', None),
            500,
            new_comment.get('message', None)
        )
    return ResponseModel(new_comment, "Comment added successfully.")

@router.get("/{community_id}/{board_id}/post/{post_id}", response_description="Communites retrieved")
async def get_comments(community_id:str, board_id:str, post_id:str, dependencies:dict=Depends(verify_token)):
    comments = await read_comments(community_id, board_id, post_id)
    if comments:
        return ResponseModel(comments, "Communites data statistic retrieved successfully")
    return ResponseModel(comments, "Empty list returned")

@router.get("/{community_id}/{board_id}/post/{post_id}/id/{id}", response_description="Communites retrieved")
async def get_comment_by_id(community_id:str, board_id:str, post_id:str, id:str, dependencies:dict=Depends(verify_token)):
    comments = await read_comment_by_id(community_id, board_id, post_id, id)
    if comments:
        return ResponseModel(comments, "Communites data statistic retrieved successfully")
    return ResponseModel(comments, "Empty list returned")

@router.get("/{community_id}/{board_id}/post/{post_id}/name/{name}", response_description="Communites retrieved")
async def get_comment_by_name(community_id:str, board_id:str, post_id:str, name:str, dependencies:dict=Depends(verify_token)):
    comments = await read_comment_by_name(community_id, board_id, post_id, name)
    if comments:
        return ResponseModel(comments, "Communites data statistic retrieved successfully")
    return ResponseModel(comments, "Empty list returned")

@router.put("/{community_id}/{board_id}/post/{post_id}/id/{id}")
async def update_comment_data(community_id:str, board_id:str, post_id:str, id: str, req: Update_comment_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    comment = jsonable_encoder(req)
    updated_comment = await update_comment(community_id, board_id, post_id, id, comment)
    if 'data' in updated_comment:
        return ResponseModel(
            "Comment with ID: {} name update is successful".format(id),
            "Comment name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the comment data.",
    )

@router.delete("/{community_id}/{board_id}/post/{post_id}/id/{id}", response_description="Comment data deleted from the database")
async def delete_comment_data(community_id:str, board_id:str, post_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_comment = await delete_comment(community_id, board_id, post_id, id)
    if deleted_comment == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )
