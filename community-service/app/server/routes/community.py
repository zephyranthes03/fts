import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.communiy import (
    read_communiy_by_id,
    read_communiy_by_name,
    read_communites,
    add_communiy,
    delete_communiy,
    update_communiy
)

from app.server.schemas.communiy import (
    ErrorResponseModel,
    ResponseModel,
    Communiy_schema,
    Update_communiy_schema
)


router = APIRouter()


@router.post("/", response_description="Communiy data folder added into the database")
async def add_communiy_data(communiy: Communiy_schema = Body(...), dependencies:dict=Depends(verify_token)):
    communiy = jsonable_encoder(communiy)
    new_communiy = await add_communiy(communiy)
    if new_communiy.get('error', None):
        return ErrorResponseModel(
            new_communiy.get('error', None),
            500,
            new_communiy.get('message', None)
        )
    return ResponseModel(new_communiy, "Communiy added successfully.")



@router.get("/", response_description="Communites retrieved")
async def get_communites(dependencies:dict=Depends(verify_token)):
    communites = await read_communites()
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.get("/id/{id}", response_description="Communites retrieved")
async def get_communiy_by_id(id:str, dependencies:dict=Depends(verify_token)):
    communites = await read_communiy_by_id(id)
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.get("/name/{name}", response_description="Communites retrieved")
async def get_communiy_by_name(name:str, dependencies:dict=Depends(verify_token)):
    communites = await read_communiy_by_name(name)
    if communites:
        return ResponseModel(communites, "Communites data statistic retrieved successfully")
    return ResponseModel(communites, "Empty list returned")

@router.put("/id/{id}")
async def update_communiy_data(id: str, req: Update_communiy_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    communiy = jsonable_encoder(req)
    updated_communiy = await update_communiy(id, communiy)
    if 'data' in updated_communiy:
        return ResponseModel(
            "Communiy with ID: {} name update is successful".format(id),
            "Communiy name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the communiy data.",
    )

@router.delete("/id/{id}", response_description="Communiy data deleted from the database")
async def delete_communiy_data(id:str, dependencies:dict=Depends(verify_token)):
    deleted_communiy = await delete_communiy(id)
    if deleted_communiy == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )