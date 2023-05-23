from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database.image import (
    add_sampleimage,
    delete_sampleimage,
    update_sampleimage,
    retrieve_sampleimages,
    retrieve_sampleimage_by_id
)
from app.server.models.diag import (
    ErrorResponseModel,
    ResponseModel,
    SampleImageSchema,
    UpdateSampleImageModel,
)

router = APIRouter()

@router.post("/", response_description="Diag data added into the database")
async def add_sampleimage(image: SampleImageSchema = Body(...)):
    image = jsonable_encoder(image)
    new_image = await add_sampleimage(image)
    return ResponseModel(new_image, "Image added successfully.")

@router.get("/", response_description="Images retrieved")
async def get_sampleimages():
    images = await retrieve_sampleimages()
    if images:
        return ResponseModel(images, "Images data retrieved successfully")
    return ResponseModel(images, "Empty list returned")

@router.get("/{id}", response_description="Image data retrieved by image_id")
async def get_sampleimage_data(id: str):
    image = await retrieve_sampleimage_by_id(id)
    if 'data' in image:
        return ResponseModel(image, "Image data retrieved successfully")
    return ResponseModel(image, "Empty list returned")

@router.put("/{id}")
async def update_sampleimage_data(id: str, req: UpdateSampleImageModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    image = jsonable_encoder(req)
    updated_image = await update_sampleimage(id, image)
    if updated_image:
        return ResponseModel(
            "Image with ID: {} name update is successful".format(id),
            "Image name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the image data.",
    )


@router.delete("/{id}")
async def delete_sampleimage_data(id: str):
    req = {k: v for k, v in req.dict().items() if v is not None}
    image = jsonable_encoder(req)
    updated_image = await delete_sampleimage(id)
    if updated_image:
        return ResponseModel(
            "Image with ID: {} name delete is successful".format(id),
            "Image name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the image data.",
    )

