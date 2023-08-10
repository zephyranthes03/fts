from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.member import (
    add_member,
    delete_member,
    update_member,
    retrieve_members,
    retrieve_member_by_id,
    retrieve_member_by_name
)

from app.server.schemas.member import (
    ErrorResponseModel,
    ResponseModel,
    Member_schema,
    Update_member_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}", response_description="Member data added into the database")
async def add_member_data(request: Request, community_id: str, member: Member_schema = Body(...)):
    member = jsonable_encoder(member)
    new_member = await add_member(request.app.mongodb_client, community_id, member)
    return ResponseModel(new_member, "Member added successfully.")

@router.get("/{community_id}", response_description="Members retrieved")
async def get_members_data(request: Request, community_id: str):
    members = await retrieve_members(request.app.mongodb_client, community_id)
    members_list = list()
    if members:
        for member in members:
            # member_dict = await member_list_to_dict(member)
            members_list.append(member)
        return members_list

    return members

@router.get("/{community_id}/id/{id}", response_description="Member data retrieved by member_id")
async def get_member_data(request: Request, community_id: str, id: str):
    member = await retrieve_member_by_id(request.app.mongodb_client, community_id, id)
    return member

@router.get("/{community_id}/name/{name}", response_description="Member data retrieved by member_id")
async def get_member_data(request: Request, community_id: str, name: str):
    member = await retrieve_member_by_name(request.app.mongodb_client, community_id, name)
    return member


@router.put("/{community_id}/id/{id}")
async def update_member_data(request: Request, community_id: str, id: str, req: Update_member_schema = Body(...)):
    member = {k: v for k, v in req.dict().items() if v is not None}

    if len(member) >= 1:
        update_result = await update_member(request.app.mongodb_client, community_id, id, member)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_member := await retrieve_member_by_id(request.app.mongodb_client, community_id, id)
    ) is not None:
        return ResponseModel(existing_member, "Member updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the member data.",
    )


@router.delete("/{community_id}/id/{id}")
async def delete_member_data(request: Request, community_id: str, id: str):
    deleted_member = await delete_member(request.app.mongodb_client, community_id, id)
    if deleted_member:
        return ResponseModel(
            "Member with ID: {} name delete is successful".format(id),
            "Member name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the member data.",
    )

