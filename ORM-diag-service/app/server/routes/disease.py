from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database.disease import (
    add_disease,
    delete_disease,
    update_disease,
    retrieve_diseases,
    retrieve_disease_by_id,
)

from app.server.models.diag import (
    ErrorResponseModel,
    ResponseModel,
    DiseaseSchema,
    UpdateDiseaseModel,
)

router = APIRouter()

@router.post("/", response_description="Diag data added into the database")
async def add_disease_data(disease: DiseaseSchema = Body(...)):
    disease = jsonable_encoder(disease)
    new_disease = await add_disease(disease)
    return ResponseModel(new_disease, "Disease added successfully.")

@router.get("/", response_description="Diseases retrieved")
async def get_diseases_data():
    diseases = await retrieve_diseases()
    if diseases:
        return ResponseModel(diseases, "Diseases data retrieved successfully")
    return ResponseModel(diseases, "Empty list returned")

@router.get("/{id}", response_description="Disease data retrieved by disease_id")
async def get_disease_data(id: str):
    disease = await retrieve_disease_by_id(id)
    if 'data' in disease:
        return ResponseModel(disease, "Disease data retrieved successfully")
    return ResponseModel(disease, "Empty list returned")

@router.put("/{id}")
async def update_disease_data(id: str, req: UpdateDiseaseModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    disease = jsonable_encoder(req)
    updated_disease = await update_disease(id, disease)
    if updated_disease:
        return ResponseModel(
            "Disease with ID: {} name update is successful".format(id),
            "Disease name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the disease data.",
    )


@router.delete("/{id}")
async def delete_disease_data(id: str):
    req = {k: v for k, v in req.dict().items() if v is not None}
    disease = jsonable_encoder(req)
    updated_disease = await delete_disease(id)
    if updated_disease:
        return ResponseModel(
            "Disease with ID: {} name delete is successful".format(id),
            "Disease name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the disease data.",
    )

