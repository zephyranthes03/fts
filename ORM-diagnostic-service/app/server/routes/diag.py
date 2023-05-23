from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database.diag import (
    add_diag,
    delete_diag,
    update_diag,
    retrieve_diags,
    retrieve_diag_by_id,
)

from app.server.models.diag import (
    ErrorResponseModel,
    ResponseModel,
    DiagSchema,
    UpdateDiagModel,
)

router = APIRouter()

@router.post("/", response_description="Diag data added into the database")
async def add_diag(diag: DiagSchema = Body(...)):
    diag = jsonable_encoder(diag)
    new_diag = await add_diag(diag)
    return ResponseModel(new_diag, "Diag added successfully.")

@router.get("/", response_description="Diags retrieved")
async def get_diags():
    diags = await retrieve_diags()
    if diags:
        return ResponseModel(diags, "Diags data retrieved successfully")
    return ResponseModel(diags, "Empty list returned")

@router.get("/{id}", response_description="Diag data retrieved by diag_id")
async def get_diag_data(id: str):
    diag = await retrieve_diag_by_id(id)
    if 'data' in diag:
        return ResponseModel(diag, "Diag data retrieved successfully")
    return ResponseModel(diag, "Empty list returned")

@router.put("/{id}")
async def update_diag_data(id: str, req: UpdateDiagModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    diag = jsonable_encoder(req)
    updated_diag = await update_diag(id, diag)
    if updated_diag:
        return ResponseModel(
            "Diag with ID: {} name update is successful".format(id),
            "Diag name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the diag data.",
    )


@router.delete("/{id}")
async def delete_diag_data(id: str):
    req = {k: v for k, v in req.dict().items() if v is not None}
    diag = jsonable_encoder(req)
    updated_diag = await delete_diag(id)
    if updated_diag:
        return ResponseModel(
            "Diag with ID: {} name delete is successful".format(id),
            "Diag name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the diag data.",
    )

