import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image
from DeepImageSearch import Load_Data, Search_Setup

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.image import (
    read_image_by_id,
    read_images,
    add_image,
    delete_image,
    update_image
)


from app.server.models.symptom import (
    ErrorResponseModel,
    ResponseModel,
    SampleImageSchema,
    UpdateSampleImageModel
)


router = APIRouter()


@router.post("/", response_description="Image data folder added into the database")
async def add_image_data(image: SampleImageSchema = Body(...), dependencies:dict=Depends(verify_token)):
    image = jsonable_encoder(image)
    new_image = await add_image(image)
    return ResponseModel(new_image, "Image added successfully.")

@router.get("/", response_description="Images retrieved")
async def get_images(dependencies:dict=Depends(verify_token)):
    images = await read_images()
    if images:
        return ResponseModel(images, "Images data statistic retrieved successfully")
    return ResponseModel(images, "Empty list returned")

@router.get("/{id}", response_description="Images retrieved")
async def get_image(id:str, dependencies:dict=Depends(verify_token)):
    images = await read_image_by_id(id)
    if images:
        return ResponseModel(images, "Images data statistic retrieved successfully")
    return ResponseModel(images, "Empty list returned")

@router.put("/{id}")
async def update_image_data(id: str, req: UpdateSampleImageModel = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    image = jsonable_encoder(req)
    updated_image = await update_image(id, image)
    if 'data' in updated_image:
        return ResponseModel(
            "Image with ID: {} name update is successful".format(id),
            "Image name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the image data.",
    )

@router.delete("/{id}", response_description="Image data deleted from the database")
async def delete_image_data(id:str, dependencies:dict=Depends(verify_token)):
    deleted_image = await delete_image(id)
    if deleted_image == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )