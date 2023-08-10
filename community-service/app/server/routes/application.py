import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

# templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.application import (
    read_application_by_id,
    read_application_by_name,
    read_applications,
    add_application,
    delete_application,
    update_application,
    join_invitation,
    join_request,
    join_response
)

from app.server.schemas.application import (
    ErrorResponseModel,
    ResponseModel,
    Application_schema,
    Update_application_schema
)


router = APIRouter()



@router.post("/{community_id}", response_description="Application data folder added into the database")
async def add_application_data(community_id:str, application: Application_schema = Body(...), dependencies:dict=Depends(verify_token)):
    application = jsonable_encoder(application)
    new_application = await add_application(community_id, application)
    if new_application.get('error', None):
        return ErrorResponseModel(
            new_application.get('error', None),
            500,
            new_application.get('message', None)
        )
    return ResponseModel(new_application, "Application added successfully.")

@router.get("/{community_id}", response_description="Communites retrieved")
async def get_applications(community_id:str, dependencies:dict=Depends(verify_token)):
    applications = await read_applications(community_id)
    if applications:
        return ResponseModel(applications, "Communites data statistic retrieved successfully")
    return ResponseModel(applications, "Empty list returned")

@router.get("/{community_id}/id/{id}", response_description="Communites retrieved")
async def get_application_by_id(community_id:str, id:str, dependencies:dict=Depends(verify_token)):
    applications = await read_application_by_id(community_id, id)
    if applications:
        return ResponseModel(applications, "Communites data statistic retrieved successfully")
    return ResponseModel(applications, "Empty list returned")

@router.get("/{community_id}/name/{name}", response_description="Communites retrieved")
async def get_application_by_name(community_id:str, name:str, dependencies:dict=Depends(verify_token)):
    applications = await read_application_by_name(community_id, name)
    if applications:
        return ResponseModel(applications, "Communites data statistic retrieved successfully")
    return ResponseModel(applications, "Empty list returned")

@router.put("/{community_id}/id/{id}")
async def update_application_data(community_id:str, id: str, req: Update_application_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    application = jsonable_encoder(req)
    updated_application = await update_application(community_id, id, application)
    if 'data' in updated_application:
        return ResponseModel(
            "Application with ID: {} name update is successful".format(id),
            "Application name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the application data.",
    )

@router.delete("/{community_id}/id/{id}", response_description="Application data deleted from the database")
async def delete_application_data(community_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_application = await delete_application(community_id, id)
    if deleted_application == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )

@router.post("/{community_id}/invite/{member_id}", response_description="Application invitation")
async def join_invitation_data(community_id:str, member_id:str, invitation_message:str, dependencies:dict=Depends(verify_token)):
    new_application = await join_invitation(community_id, member_id, invitation_message)
    if new_application.get('error', None):
        return ErrorResponseModel(
            new_application.get('error', None),
            500,
            new_application.get('message', None)
        )
    return ResponseModel(new_application, "Application added successfully.")

@router.post("/{community_id}/request", response_description="Application apply to the community")
async def join_request_data(community_id:str, member_id:str, invitaion_message: dict, dependencies:dict=Depends(verify_token)):
    request_form = jsonable_encoder(request_form)
    new_application = await join_response(community_id, member_id, request_form)
    if new_application.get('error', None):
        return ErrorResponseModel(
            new_application.get('error', None),
            500,
            new_application.get('message', None)
        )
    return ResponseModel(new_application, "Application added successfully.")

@router.post("/{community_id}/response", response_description="Application application permit from the community admin")
async def join_response_data(community_id:str, member_id:str, response_message:str, dependencies:dict=Depends(verify_token)):
    new_application = await join_response(community_id, member_id, response_message)
    if new_application.get('error', None):
        return ErrorResponseModel(
            new_application.get('error', None),
            500,
            new_application.get('message', None)
        )
    return ResponseModel(new_application, "Application added successfully.")


# Delete a application from the database
async def join_request(community_id:str, member_id:str, invitation_message:str):
    pass
\
# Delete a application from the database
async def join_response(community_id:str, member_id:str, invitation_message:str):
    pass
