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

from app.server.process.member import (
    read_member_by_id,
    read_member_by_name,
    read_members,
    add_member,
    delete_member,
    update_member,
)

from app.server.schemas.member import (
    ErrorResponseModel,
    ResponseModel,
    Member_schema,
    Update_member_schema
)


router = APIRouter()



@router.post("/{community_id}", response_description="Member data folder added into the database")
async def add_member_data(community_id:str, member: Member_schema = Body(...), dependencies:dict=Depends(verify_token)):
    member = jsonable_encoder(member)
    new_member = await add_member(community_id, member)
    if new_member.get('error', None):
        return ErrorResponseModel(
            new_member.get('error', None),
            500,
            new_member.get('message', None)
        )
    return ResponseModel(new_member, "Member added successfully.")

@router.get("/{community_id}", response_description="Communites retrieved")
async def get_members(community_id:str, dependencies:dict=Depends(verify_token)):
    members = await read_members(community_id)
    if members:
        return ResponseModel(members, "Communites data statistic retrieved successfully")
    return ResponseModel(members, "Empty list returned")

@router.get("/{community_id}/id/{id}", response_description="Communites retrieved")
async def get_member_by_id(community_id:str, id:str, dependencies:dict=Depends(verify_token)):
    members = await read_member_by_id(community_id, id)
    if members:
        return ResponseModel(members, "Communites data statistic retrieved successfully")
    return ResponseModel(members, "Empty list returned")

@router.get("/{community_id}/name/{name}", response_description="Communites retrieved")
async def get_member_by_name(community_id:str, name:str, dependencies:dict=Depends(verify_token)):
    members = await read_member_by_name(community_id, name)
    if members:
        return ResponseModel(members, "Communites data statistic retrieved successfully")
    return ResponseModel(members, "Empty list returned")

@router.put("/{community_id}/id/{id}")
async def update_member_data(community_id:str, id: str, req: Update_member_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    member = jsonable_encoder(req)
    updated_member = await update_member(community_id, id, member)
    if 'data' in updated_member:
        return ResponseModel(
            "Member with ID: {} name update is successful".format(id),
            "Member name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the member data.",
    )

@router.delete("/{community_id}/id/{id}", response_description="Member data deleted from the database")
async def delete_member_data(community_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_member = await delete_member(community_id, id)
    if deleted_member == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )
