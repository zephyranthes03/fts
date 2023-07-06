from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.databases.symptom_index import (
    add_symptom_index,
    delete_symptom_index,
    update_symptom_index,
    retrieve_symptom_indexes,
    retrieve_symptom_index_by_id,
    retrieve_symptom_index_by_name
)

from app.server.schemas.symptom_index import (
    ErrorResponseModel,
    ResponseModel,
    Symptom_index_schema,
    Update_symptom_index_schema,
)

router = APIRouter()


@router.post("/", response_description="Symptom data added into the database")
async def add_symptom_index_data(request: Request, symptom: Symptom_index_schema = Body(...)):
    symptom = jsonable_encoder(symptom)
    new_symptom_index = await add_symptom_index(request.app.database['symptom_indexes'], symptom)
    return ResponseModel(new_symptom_index, "Symptom added successfully.")

@router.get("/", response_description="Symptoms retrieved")
async def get_symptom_indexes_data(request: Request):
    symptom_indexes = await retrieve_symptom_indexes(request.app.database['symptom_indexes'])
    symptom_indexes_list = list()
    if symptom_indexes:
        for symptom_index in symptom_indexes:
            # symptom_index_dict = await symptom_index_list_to_dict(symptom)
            symptom_indexes_list.append(symptom_index)
        return symptom_indexes_list

    return symptom_indexes

@router.get("/id/{id}", response_description="Symptom data retrieved by symptom_id")
async def get_symptom_index_data_by_id(request: Request, id: str):
    symptom = await retrieve_symptom_index_by_id(request.app.database['symptom_indexes'], id)
    return symptom

@router.get("/name/{name}", response_description="Symptom data retrieved by symptom name")
async def get_symptom_index_data_by_name(request: Request, name: str):
    symptom = await retrieve_symptom_index_by_name(request.app.database['symptom_indexes'], name)
    return symptom

@router.put("/{id}")
async def update_symptom_index_data(request: Request, id: str, req: Update_symptom_index_schema = Body(...)):
    symptom_index = {k: v for k, v in req.dict().items() if v is not None}

    if len(symptom_index) >= 1:
        update_result = await update_symptom_index(request.app.database["symptom_indexes"], id, symptom)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_symptom_index := await retrieve_symptom_index_by_id(request.app.database['symptom_indexes'], id)
    ) is not None:
        return ResponseModel(existing_symptom_index, "Symptom_index updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the symptom_index data.",
    )


@router.delete("/{id}")
async def delete_symptom_index_data(request: Request, id: str):
    deleted_symptom_index = await delete_symptom_index(request.app.database['symptom_indexes'], id)
    if deleted_symptom_index:
        return ResponseModel(
            "Symptom_index with ID: {} name delete is successful".format(id),
            "Symptom_index name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the symptom_index data.",
    )


