from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from app.server.databases.symptom import (
    add_symptom,
    delete_symptom,
    update_symptom,
    retrieve_symptoms,
    retrieve_symptom_by_id,
)

from app.server.schemas.symptom import (
    ErrorResponseModel,
    ResponseModel,
    SymptomSchema,
    UpdateSymptomModel,
)

from app.server.util.convert import symptom_list_to_dict


router = APIRouter()


@router.post("/", response_description="Symptom data added into the database")
async def add_symptom_data(request: Request, symptom: SymptomSchema = Body(...)):
    symptom = jsonable_encoder(symptom)
    new_symptom = await add_symptom(request.app.database['symptoms'], symptom)
    return ResponseModel(new_symptom, "Symptom added successfully.")

@router.get("/", response_description="Symptoms retrieved")
async def get_symptoms_data(request: Request):
    symptoms = await retrieve_symptoms(request.app.database['symptoms'])
    symptoms_list = list()
    if symptoms:
        for symptom in symptoms:
            # symptom_dict = await symptom_list_to_dict(symptom)
            symptoms_list.append(symptom)
        return symptoms_list

    return symptoms

@router.get("/{id}", response_description="Symptom data retrieved by symptom_id")
async def get_symptom_data(request: Request, id: str):
    symptom = await retrieve_symptom_by_id(request.app.database['symptoms'], id)
    return symptom

@router.put("/{id}")
async def update_symptom_data(request: Request, id: str, req: UpdateSymptomModel = Body(...)):
    symptom = {k: v for k, v in req.dict().items() if v is not None}

    if len(symptom) >= 1:
        update_result = await update_symptom(request.app.database["symptoms"], id, symptom)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_symptom := await retrieve_symptom_by_id(request.app.database['symptoms'], id)
    ) is not None:
        return ResponseModel(existing_symptom, "Symptom updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the symptom data.",
    )


@router.delete("/{id}")
async def delete_symptom_data(request: Request, id: str):
    deleted_symptom = await delete_symptom(request.app.database['symptoms'], id)
    if deleted_symptom:
        return ResponseModel(
            "Symptom with ID: {} name delete is successful".format(id),
            "Symptom name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the symptom data.",
    )


