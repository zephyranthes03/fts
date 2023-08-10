from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.application import (
    add_application,
    delete_application,
    update_application,
    retrieve_applications,
    retrieve_application_by_id,
)

from app.server.schemas.application import (
    ErrorResponseModel,
    ResponseModel,
    Application_schema,
    Update_application_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}", response_description="Application data added into the database")
async def add_application_data(request: Request, community_id: str, application: Application_schema = Body(...)):
    application = jsonable_encoder(application)
    new_application = await add_application(request.app.mongodb_client, community_id, application)
    return ResponseModel(new_application, "Application added successfully.")

@router.get("/{community_id}", response_description="Applications retrieved")
async def get_applications_data(request: Request, community_id: str):
    applications = await retrieve_applications(request.app.mongodb_client, community_id)
    applications_list = list()
    if applications:
        for application in applications:
            # application_dict = await application_list_to_dict(application)
            applications_list.append(application)
        return applications_list

    return applications

@router.get("/{community_id}/id/{id}", response_description="Application data retrieved by application_id")
async def get_application_data(request: Request, community_id: str, id: str):
    application = await retrieve_application_by_id(request.app.mongodb_client, community_id, id)
    return application


@router.put("/{community_id}/id/{id}")
async def update_application_data(request: Request, community_id: str, id: str, req: Update_application_schema = Body(...)):
    application = {k: v for k, v in req.dict().items() if v is not None}

    if len(application) >= 1:
        update_result = await update_application(request.app.mongodb_client, id, application)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_application := await retrieve_application_by_id(request.app.database[community_id], id)
    ) is not None:
        return ResponseModel(existing_application, "Application updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the application data.",
    )


@router.delete("/{community_id}/id/{id}")
async def delete_application_data(request: Request, community_id: str, id: str):
    deleted_application = await delete_application(request.app.mongodb_client, community_id, id)
    if deleted_application:
        return ResponseModel(
            "Application with ID: {} name delete is successful".format(id),
            "Application name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the application data.",
    )

