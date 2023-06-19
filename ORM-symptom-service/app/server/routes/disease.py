from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.disease import (
    add_disease,
    delete_disease,
    update_disease,
    retrieve_diseases,
    retrieve_disease_by_id,
)

from app.server.schemas.disease import (
    ErrorResponseModel,
    ResponseModel,
    DiseaseSchema,
    UpdateDiseaseModel,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/", response_description="Disease data added into the database")
async def add_disease_data(request: Request, disease: DiseaseSchema = Body(...)):
    disease = jsonable_encoder(disease)
    new_disease = await add_disease(request.app.database['diseases'], disease)
    return ResponseModel(new_disease, "Disease added successfully.")

@router.get("/", response_description="Diseases retrieved")
async def get_diseases_data(request: Request):
    diseases = await retrieve_diseases(request.app.database['diseases'])
    diseases_list = list()
    if diseases:
        for disease in diseases:
            # disease_dict = await disease_list_to_dict(disease)
            diseases_list.append(disease)
        return diseases_list

    return diseases

@router.get("/{id}", response_description="Disease data retrieved by disease_id")
async def get_disease_data(request: Request, id: str):
    disease = await retrieve_disease_by_id(request.app.database['diseases'], id)
    return disease

@router.put("/{id}")
async def update_disease_data(request: Request, id: str, req: UpdateDiseaseModel = Body(...)):
    disease = {k: v for k, v in req.dict().items() if v is not None}

    if len(disease) >= 1:
        update_result = await update_disease(request.app.database["diseases"], id, disease)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_disease := await retrieve_disease_by_id(request.app.database['diseases'], id)
    ) is not None:
        return ResponseModel(existing_disease, "Disease updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the disease data.",
    )


@router.delete("/{id}")
async def delete_disease_data(request: Request, id: str):
    deleted_disease = await delete_disease(request.app.database['diseases'], id)
    if deleted_disease:
        return ResponseModel(
            "Disease with ID: {} name delete is successful".format(id),
            "Disease name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the disease data.",
    )

