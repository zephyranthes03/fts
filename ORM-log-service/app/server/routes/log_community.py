from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.log_community import (
    add_log_community,
    delete_log_community,
    update_log_community,
    retrieve_Log_communities,
    retrieve_log_community_by_id,
)

from app.server.schemas.log_community import (
    ErrorResponseModel,
    ResponseModel,
    log_community_schema,
    Update_log_community_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}/{user_id}", response_description="log_community data added into the database")
async def add_log_community_data(request: Request, community_id: str, user_id: str, log_community: log_community_schema = Body(...)):
    log_community = jsonable_encoder(log_community)
    new_log_community = await add_log_community(request.app.mongodb_client,
                                community_id, user_id,
                                log_community)
    return ResponseModel(new_log_community, "log_community added successfully.")

@router.get("/{community_id}/{user_id}", response_description="Log_communities retrieved")
async def get_Log_communities_data(request: Request, community_id: str, user_id: str,
                          page: int = 1, size: int = 10, search_keyword: str = ""):
    Log_communities = await retrieve_Log_communities(request.app.mongodb_client,
                                   community_id, user_id,
                                   page, size, search_keyword)
    Log_communities_list = list()
    if Log_communities:
        for log_community in Log_communities:
            # log_community_dict = await log_community_list_to_dict(log_community)
            Log_communities_list.append(log_community)
        return Log_communities_list

    return Log_communities

@router.get("/{community_id}/{user_id}/{id}", response_description="log_community data retrieved by user_id")
async def get_log_community_data(request: Request, community_id: str, user_id: str, id: str):
    log_community = await retrieve_log_community_by_id(request.app.mongodb_client,
                                       community_id, user_id,
                                       id)
    return log_community

@router.put("/{community_id}/{user_id}/{id}")
async def update_log_community_data(request: Request, community_id: str, user_id: str, id: str, req: Update_log_community_schema = Body(...)):
    log_community = {k: v for k, v in req.dict().items() if v is not None}

    if len(log_community) >= 1:
        update_result = await update_log_community(request.app.mongodb_client,
                                           community_id, user_id,
                                           id, log_community)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_log_community := await retrieve_log_community_by_id(request.app.mongodb_client,
                                                     community_id, user_id, id)
    ) is not None:
        return ResponseModel(existing_log_community, "log_community updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the log_community data.",
    )


@router.delete("/{community_id}/{user_id}/{id}")
async def delete_log_community_data(request: Request, community_id: str, user_id: str, id: str):
    deleted_log_community = await delete_log_community(request.app.mongodb_client,
                                       community_id, user_id,
                                       id)
    if deleted_log_community:
        return ResponseModel(
            "log_community with ID: {} name delete is successful".format(id),
            "log_community name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the log_community data.",
    )

