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

from app.server.process.post import (
    read_post_by_id,
    like_post_by_id,
    read_post_by_name,
    read_posts,
    add_post,
    delete_post,
    update_post,
)

from app.server.schemas.post import (
    ErrorResponseModel,
    ResponseModel,
    Post_schema,
    Update_post_schema
)


router = APIRouter()



@router.post("/{community_id}/{board_id}", response_description="Post data folder added into the database")
async def add_post_data(community_id:str, board_id:str, post: Post_schema = Body(...), dependencies:dict=Depends(verify_token)):
    post = jsonable_encoder(post)
    new_post = await add_post(community_id, board_id, post)
    if new_post.get('error', None):
        return ErrorResponseModel(
            new_post.get('error', None),
            500,
            new_post.get('message', None)
        )
    return ResponseModel(new_post, "Post added successfully.")

@router.get("/{community_id}/{board_id}", response_description="Posting thread on the community")
async def get_posts(community_id:str, board_id:str, dependencies:dict=Depends(verify_token)):
    posts = await read_posts(community_id, board_id)
    if posts:
        return ResponseModel(posts, "Communites data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.get("/{community_id}/{board_id}/read/{id}", response_description="Communites post retrieved")
async def get_post_by_id(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    posts = await read_post_by_id(community_id, board_id, id)
    if posts:
        return ResponseModel(posts, "Communites data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.get("/{community_id}/{board_id}/like/{id}", response_description="Communites retrieved")
async def get_post_by_id(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    print(dependencies,flush=True)
    posts = await like_post_by_id(community_id, board_id, id, dependencies)
    if posts:
        return ResponseModel(posts, "Communites data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")


@router.get("/{community_id}/{board_id}/name/{name}", response_description="Communites retrieved")
async def get_post_by_name(community_id:str, board_id:str, name:str, dependencies:dict=Depends(verify_token)):
    posts = await read_post_by_name(community_id, board_id, name)
    if posts:
        return ResponseModel(posts, "Communites data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.put("/{community_id}/{board_id}/id/{id}")
async def update_post_data(community_id:str, board_id:str, id: str, req: Update_post_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    post = jsonable_encoder(req)
    updated_post = await update_post(community_id, board_id, id, post)
    if 'data' in updated_post:
        return ResponseModel(
            "Post with ID: {} name update is successful".format(id),
            "Post name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the post data.",
    )

@router.delete("/{community_id}/{board_id}/id/{id}", response_description="Post data deleted from the database")
async def delete_post_data(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_post = await delete_post(community_id, board_id, id)
    if deleted_post == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )
