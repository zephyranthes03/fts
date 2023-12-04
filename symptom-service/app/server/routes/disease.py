import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
# from PIL import Image
from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

# templates = Jinja2Templates(directory="app/templates")

metadata = None 
st = None
from app.server.process.disease import (
    read_disease_by_id,
    read_disease_by_name,
    read_diseases,
    add_disease,
    delete_disease,
    update_disease
)

from app.server.schemas.disease import (
    ErrorResponseModel,
    ResponseModel,
    Disease_schema,
    Update_disease_schema,
)


router = APIRouter()


@router.post("/", response_description="Disease data folder added into the database")
async def add_disease_data(disease: Disease_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    disease = jsonable_encoder(disease)
    new_disease = await add_disease(disease)
    if new_disease.get('error', None):
        return ErrorResponseModel(
            new_disease.get('error', None),
            500,
            new_disease.get('message', None)
        )

    return ResponseModel(new_disease, "Disease added successfully.")

@router.get("/", response_description="Diseases retrieved")
async def get_diseases(): #dependencies:dict=Depends(verify_token)):
    diseases = await read_diseases()
    if diseases:
        return ResponseModel(diseases, "Diseases data statistic retrieved successfully")
    return ResponseModel(diseases, "Empty list returned")

@router.get("/id/{id}", response_description="Diseases retrieved")
async def get_disease_by_id(id:str): #, dependencies:dict=Depends(verify_token)):
    diseases = await read_disease_by_id(id)
    if diseases:
        return ResponseModel(diseases, "Diseases data statistic retrieved successfully")
    return ResponseModel(diseases, "Empty list returned")

@router.get("/name/{name}", response_description="Diseases retrieved")
async def get_disease_by_name(name:str): #, dependencies:dict=Depends(verify_token)):
    diseases = await read_disease_by_name(name)
    if diseases:
        return ResponseModel(diseases, "Diseases data statistic retrieved successfully")
    return ResponseModel(diseases, "Empty list returned")

@router.put("/id/{id}")
async def update_disease_data(id: str, req: Update_disease_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    disease = jsonable_encoder(req)
    updated_disease = await update_disease(id, disease)
    if 'data' in updated_disease:
        return ResponseModel(
            "Disease with ID: {} name update is successful".format(id),
            "Disease name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the disease data.",
    )

@router.delete("/id/{id}", response_description="Disease data deleted from the database")
async def delete_disease_data(id:str): #, dependencies:dict=Depends(verify_token)):
    deleted_disease = await delete_disease(id)
    if deleted_disease == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )