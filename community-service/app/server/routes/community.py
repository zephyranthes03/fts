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

from app.server.process.community import (
    read_community_by_id,
    read_community_by_name,
    read_communities,
    add_community,
    delete_community,
    update_community
)

from app.server.schemas.community import (
    ErrorResponseModel,
    ResponseModel,
    Community_schema,
    Update_community_schema
)


router = APIRouter()


@router.post("/", response_description="Communiy data folder added into the database")
async def add_community_data(community: Community_schema = Body(...), dependencies:dict=Depends(verify_token)):
    community = jsonable_encoder(community)
    new_community = await add_community(community)
    if new_community.get('error', None):
        return ErrorResponseModel(
            new_community.get('error', None),
            500,
            new_community.get('message', None)
        )
    return ResponseModel(new_community, "Communiy added successfully.")



@router.get("/", response_description="Communites retrieved")
async def get_communites(dependencies:dict=Depends(verify_token)):
    communites = await read_communities()
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.get("/id/{id}", response_description="Communites retrieved")
async def get_community_by_id(id:str, dependencies:dict=Depends(verify_token)):
    communites = await read_community_by_id(id)
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.get("/name/{name}", response_description="Communites retrieved")
async def get_community_by_name(name:str, dependencies:dict=Depends(verify_token)):
    communites = await read_community_by_name(name)
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.put("/id/{id}")
async def update_community_data(id: str, req: Update_community_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    community = jsonable_encoder(req)
    updated_community = await update_community(id, community)
    if 'data' in updated_community:
        return ResponseModel(
            "Communiy with ID: {} name update is successful".format(id),
            "Communiy name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the community data.",
    )

@router.delete("/id/{id}", response_description="Communiy data deleted from the database")
async def delete_community_data(id:str, dependencies:dict=Depends(verify_token)):
    deleted_community = await delete_community(id)
    if deleted_community == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )