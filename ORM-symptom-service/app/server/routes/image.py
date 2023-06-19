from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.databases.image import (
    add_sampleimage,
    delete_sampleimage,
    update_sampleimage,
    retrieve_sampleimages,
    retrieve_sampleimage_by_id
)
from app.server.schemas.images import (
    ErrorResponseModel,
    ResponseModel,
    SampleImageSchema,
    UpdateSampleImageModel,
)

router = APIRouter()


@router.post("/", response_description="SampleImage data added into the database")
async def add_sampleimage_data(request: Request, sampleimage: SampleImageSchema = Body(...)):
    sampleimage = jsonable_encoder(sampleimage)
    new_sampleimage = await add_sampleimage(request.app.database['sampleimages'], sampleimage)
    return ResponseModel(new_sampleimage, "SampleImage added successfully.")

@router.get("/", response_description="SampleImages retrieved")
async def get_sampleimages_data(request: Request):
    sampleimages = await retrieve_sampleimages(request.app.database['sampleimages'])
    sampleimages_list = list()
    if sampleimages:
        for sampleimage in sampleimages:
            # sampleimage_dict = await sampleimage_list_to_dict(sampleimage)
            sampleimages_list.append(sampleimage)
        return sampleimages_list

    return sampleimages

@router.get("/{id}", response_description="SampleImage data retrieved by sampleimage_id")
async def get_sampleimage_data(request: Request, id: str):
    sampleimage = await retrieve_sampleimage_by_id(request.app.database['sampleimages'], id)
    return sampleimage

@router.put("/{id}")
async def update_sampleimage_data(request: Request, id: str, req: UpdateSampleImageModel = Body(...)):
    sampleimage = {k: v for k, v in req.dict().items() if v is not None}

    if len(sampleimage) >= 1:
        update_result = await update_sampleimage(request.app.database["sampleimages"], id, sampleimage)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_sampleimage := await retrieve_sampleimage_by_id(request.app.database['sampleimages'], id)
    ) is not None:
        return ResponseModel(existing_sampleimage, "SampleImage updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the sampleimage data.",
    )


@router.delete("/{id}")
async def delete_sampleimage_data(request: Request, id: str):
    deleted_sampleimage = await delete_sampleimage(request.app.database['sampleimages'], id)
    if deleted_sampleimage:
        return ResponseModel(
            "SampleImage with ID: {} name delete is successful".format(id),
            "SampleImage name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the SampleImage data.",
    )

