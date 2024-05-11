import os
from datetime import datetime

from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder

from typing import List

from app.config.config import settings

from app.server.databases.community import (
    add_community,
    delete_community,
    update_community,
    retrieve_communities,
    retrieve_community_by_id,
    retrieve_community_by_name
)
from app.server.schemas.community import (
    ErrorResponseModel,
    ResponseModel,
    Community_schema,
    Update_community_schema,
)
from app.server.util.logging import logger

router = APIRouter()

@router.post("/", response_description="Community data added into the database")
async def add_community_data(request: Request, community: Community_schema = Body(...)):
    community = jsonable_encoder(community)
    new_community = await add_community(request.app.mongodb_client, community)
    return ResponseModel(new_community, "Community added successfully.")

@router.get("/", response_description="Communities retrieved")
async def get_communities_data(request: Request):
    communities = await retrieve_communities(request.app.mongodb_client)
    communities_list = list()
    if communities:
        for community in communities:
            # community_dict = await community_list_to_dict(community)
            communities_list.append(community)
        return communities_list

    return communities

@router.get("/id/{id}", response_description="Community data retrieved by community_id")
async def get_community_data(request: Request, id: str):
    community = await retrieve_community_by_id(request.app.mongodb_client, id)
    return community

@router.get("/name/{name}", response_description="Community data retrieved by community name")
async def get_community_data(request: Request, name: str):
    community = await retrieve_community_by_name(request.app.mongodb_client, name)
    return community

@router.put("/id/{id}")
async def update_community_data(request: Request, id: str, req: Update_community_schema = Body(...)):
    community = {k: v for k, v in req.dict().items() if v is not None}

    if len(community) >= 1:
        update_result = await update_community(request.app.mongodb_client, id, community)
        logger.info(update_result.modified_count)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_community := await retrieve_community_by_id(request.app.mongodb_client, id)
    ) is not None:
        return ResponseModel(existing_community, "Community updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the community data.",
    )


@router.delete("/id/{id}")
async def delete_community_data(request: Request, id: str):
    deleted_community = await delete_community(request.app.mongodb_client, id)
    if deleted_community:
        return ResponseModel(
            "Community with ID: {} name delete is successful".format(id),
            "Community name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Community data.",
    )
