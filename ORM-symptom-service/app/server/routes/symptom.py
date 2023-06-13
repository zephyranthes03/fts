from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database.symptom import (
    add_symptom,
    delete_symptom,
    update_symptom,
    retrieve_symptoms,
    retrieve_symptom_by_id,
)

from app.server.models.symptom import (
    ErrorResponseModel,
    ResponseModel,
    SymptomSchema,
    UpdateSymptomModel,
)

from app.server.util.convert import symptom_list_to_dict


router = APIRouter()

@router.post("/", response_description="Symptom data added into the database")
async def add_symptom_data(symptom: SymptomSchema = Body(...)):
    symptom = jsonable_encoder(symptom)
    new_symptom = await add_symptom(symptom)
    return ResponseModel(new_symptom, "Symptom added successfully.")

@router.get("/", response_description="Symptoms retrieved")
async def get_symptoms_data():
    symptoms = await retrieve_symptoms()
    symptoms_list = list()
    if symptoms:
        for symptom in symptoms:
            symptom_dict = await symptom_list_to_dict(symptom)
            symptoms_list.append(symptom_dict) 
        return symptoms_list

    return symptoms

@router.get("/{id}", response_description="Symptom data retrieved by symptom_id")
async def get_symptom_data(id: str):
    symptom = await retrieve_symptom_by_id(id)
    symptom_dict = dict()
    if symptom:
        symptom_dict = await symptom_list_to_dict(symptom)
        return symptom_dict
    return symptom

@router.put("/{id}")
async def update_symptom_data(id: str, req: UpdateSymptomModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    symptom = jsonable_encoder(req)
    updated_symptom = await update_symptom(id, symptom)
    if updated_symptom:
        return ResponseModel(
            "Symptom with ID: {} name update is successful".format(id),
            "Symptom name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the symptom data.",
    )


@router.delete("/{id}")
async def delete_symptom_data(id: str):
    req = {k: v for k, v in req.dict().items() if v is not None}
    symptom = jsonable_encoder(req)
    updated_symptom = await delete_symptom(id)
    if updated_symptom:
        return ResponseModel(
            "Symptom with ID: {} name delete is successful".format(id),
            "Symptom name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the symptom data.",
    )

