from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.databases.diagnosis import (
    add_diagnosis,
    delete_diagnosis,
    update_diagnosis,
    retrieve_diagnosises,
    retrieve_diagnosis_by_id
)
from app.server.schemas.diagnosis import (
    ErrorResponseModel,
    ResponseModel,
    Diagnosis_schema,
    Update_diagnosis_schema,
)

router = APIRouter()


@router.post("/", response_description="Diagnosis data added into the database")
async def add_diagnosis_data(request: Request, diagnosis: Diagnosis_schema = Body(...)):
    diagnosis = jsonable_encoder(diagnosis)
    new_diagnosis = await add_diagnosis(request.app.database['diagnosises'], diagnosis)
    return ResponseModel(new_diagnosis, "Diagnosis added successfully.")

@router.get("/", response_description="Communities retrieved")
async def get_diagnosises_data(request: Request):
    diagnosises = await retrieve_diagnosises(request.app.database['diagnosises'])
    diagnosises_list = list()
    if diagnosises:
        for diagnosis in diagnosises:
            # diagnosis_dict = await diagnosis_list_to_dict(diagnosis)
            diagnosises_list.append(diagnosis)
        return diagnosises_list

    return diagnosises

@router.get("/{id}", response_description="Diagnosis data retrieved by diagnosis_id")
async def get_diagnosis_data(request: Request, id: str):
    diagnosis = await retrieve_diagnosis_by_id(request.app.database['diagnosises'], id)
    return diagnosis

@router.put("/{id}")
async def update_diagnosis_data(request: Request, id: str, req: Update_diagnosis_schema = Body(...)):
    diagnosis = {k: v for k, v in req.dict().items() if v is not None}

    if len(diagnosis) >= 1:
        update_result = await update_diagnosis(request.app.database["diagnosises"], id, diagnosis)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_diagnosis := await retrieve_diagnosis_by_id(request.app.database['diagnosises'], id)
    ) is not None:
        return ResponseModel(existing_diagnosis, "Diagnosis updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the diagnosis data.",
    )


@router.delete("/{id}")
async def delete_diagnosis_data(request: Request, id: str):
    deleted_diagnosis = await delete_diagnosis(request.app.database['diagnosises'], id)
    if deleted_diagnosis:
        return ResponseModel(
            "Diagnosis with ID: {} name delete is successful".format(id),
            "Diagnosis name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Diagnosis data.",
    )

