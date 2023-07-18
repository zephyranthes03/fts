import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.diagnosis import (
    read_diagnosis_by_id,
    read_diagnosis_by_name,
    read_diagnosises,
    add_diagnosis,
    delete_diagnosis,
    update_diagnosis
)

from app.server.schemas.diagnosis import (
    ErrorResponseModel,
    ResponseModel,
    Diagnosis_schema,
    Update_diagnosis_schema
)


router = APIRouter()


@router.post("/", response_description="Diagnosis data folder added into the database")
async def add_diagnosis_data(diagnosis: Diagnosis_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    diagnosis = jsonable_encoder(diagnosis)
    new_diagnosis = await add_diagnosis(diagnosis)
    if new_diagnosis.get('error', None):
        return ErrorResponseModel(
            new_diagnosis.get('error', None),
            500,
            new_diagnosis.get('message', None)
        )
    return ResponseModel(new_diagnosis, "Diagnosis added successfully.")



@router.get("/", response_description="Diagnosises retrieved")
async def get_diagnosises(): # dependencies:dict=Depends(verify_token)):
    diagnosises = await read_diagnosises()
    if diagnosises:
        return ResponseModel(diagnosises, "Diagnosises data statistic retrieved successfully")
    return ResponseModel(diagnosises, "Empty list returned")

@router.get("/id/{id}", response_description="Diagnosises retrieved")
async def get_diagnosis_by_id(id:str): #, dependencies:dict=Depends(verify_token)):
    diagnosises = await read_diagnosis_by_id(id)
    if diagnosises:
        return ResponseModel(diagnosises, "Diagnosises data statistic retrieved successfully")
    return ResponseModel(diagnosises, "Empty list returned")

@router.get("/name/{name}", response_description="Diagnosises retrieved")
async def get_diagnosis_by_name(name:str): #, dependencies:dict=Depends(verify_token)):
    diagnosises = await read_diagnosis_by_name(name)
    if diagnosises:
        return ResponseModel(diagnosises, "Diagnosises data statistic retrieved successfully")
    return ResponseModel(diagnosises, "Empty list returned")

@router.put("/id/{id}")
async def update_diagnosis_data(id: str, req: Update_diagnosis_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    diagnosis = jsonable_encoder(req)
    updated_diagnosis = await update_diagnosis(id, diagnosis)
    if 'data' in updated_diagnosis:
        return ResponseModel(
            "Diagnosis with ID: {} name update is successful".format(id),
            "Diagnosis name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the diagnosis data.",
    )

@router.delete("/id/{id}", response_description="Diagnosis data deleted from the database")
async def delete_diagnosis_data(id:str): #, dependencies:dict=Depends(verify_token)):
    deleted_diagnosis = await delete_diagnosis(id)
    if deleted_diagnosis == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )