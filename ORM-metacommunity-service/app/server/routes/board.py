from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.community_board import (
    add_community_board,
    delete_community_board,
    update_community_board,
    retrieve_community_boards,
    retrieve_community_board_by_id,
    retrieve_community_board_by_name
)

from app.server.schemas.community_board import (
    ErrorResponseModel,
    ResponseModel,
    Community_board_schema,
    Update_community_board_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{community_id}", response_description="Community Board data added into the database")
async def add_community_board_data(request: Request, community_id: str, community_board: Community_board_schema = Body(...)):
    print(community_id,flush=True)
    community_board = jsonable_encoder(community_board)
    print(board,flush=True)
    new_community_board = await add_community_board(request.app.database['community_boards'], community_board)
    return ResponseModel(new_community_board, "Community Board added successfully.")

@router.get("/{community_id}", response_description="Community Board retrieved")
async def get_community_boards_data(request: Request, community_id: str):
    community_boards = await retrieve_community_boards(request.app.database['community_boards'])
    community_boards_list = list()
    if community_boards:
        for board in community_boards:
            # board_dict = await board_list_to_dict(board)
            community_boards_list.append(board)
        return community_boards_list

    return boards

@router.get("/{community_id}/id/{id}", response_description="Community Board data retrieved by board_id")
async def get_community_board_data(request: Request, community_id: str, id: str):
    community_board = await retrieve_community_board_by_id(request.app.database['community_boards'], id)
    return community_board

@router.get("/{community_id}/name/{name}", response_description="Community Board data retrieved by board name field")
async def get_community_board_data(request: Request, community_id: str, name: str):
    community_board = await retrieve_community_board_by_name(request.app.database['community_boards'], name)
    return community_board


@router.put("/{community_id}/id/{id}")
async def update_community_board_data(request: Request, community_id: str, id: str, req: Update_community_board_schema = Body(...)):
    community_board = {k: v for k, v in req.dict().items() if v is not None}

    if len(community_board) >= 1:
        update_result = await update_community_board(request.app.database["community_boards"], id, community_board)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_community_board := await retrieve_community_board_by_id(request.app.database['community_boards'], id)
    ) is not None:
        return ResponseModel(existing_community_board, "Community Board updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the board data.",
    )


@router.delete("/{community_id}/id/{id}")
async def delete_board_data(request: Request, community_id: str, id: str):
    deleted_community_board = await delete_community_board(request.app.database['boards'], id)
    if deleted_community_board:
        return ResponseModel(
            "Community Board with ID: {} name delete is successful".format(id),
            "Community Board name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Community Board data.",
    )

