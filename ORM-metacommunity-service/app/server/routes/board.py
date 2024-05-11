from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.board import (
    add_board,
    delete_board,
    update_board,
    retrieve_boards,
    retrieve_board_by_id,
    retrieve_board_by_name
)

from app.server.schemas.board import (
    ErrorResponseModel,
    ResponseModel,
    Board_schema,
    Update_board_schema,
)

# from app.server.databases.session import get_db
from app.server.util.logging import logger


router = APIRouter()

@router.post("/{community_id}", response_description="Community Board data added into the database")
async def add_board_data(request: Request, community_id: str, board: Board_schema = Body(...)):
    logger.info(community_id)
    board = jsonable_encoder(board)
    logger.info(board)
    new_board = await add_board(request.app.mongodb_client, community_id, board)
    return ResponseModel(new_board, "Community Board added successfully.")

@router.get("/{community_id}", response_description="Community Board retrieved")
async def get_boards_data(request: Request, community_id: str):
    boards = await retrieve_boards(request.app.mongodb_client, community_id)
    boards_list = list()
    if boards:
        for board in boards:
            # board_dict = await board_list_to_dict(board)
            boards_list.append(board)
        return boards_list

    return boards

@router.get("/{community_id}/id/{id}", response_description="Community Board data retrieved by board_id")
async def get_board_data(request: Request, community_id: str, id: str):
    board = await retrieve_board_by_id(request.app.mongodb_client, community_id, id)
    return board

@router.get("/{community_id}/name/{name}", response_description="Community Board data retrieved by board name field")
async def get_board_data(request: Request, community_id: str, name: str):
    board = await retrieve_board_by_name(request.app.mongodb_client, community_id, name)
    return board


@router.put("/{community_id}/id/{id}")
async def update_board_data(request: Request, community_id: str, id: str, req: Update_board_schema = Body(...)):
    board = {k: v for k, v in req.dict().items() if v is not None}

    if len(board) >= 1:
        update_result = await update_board(request.app.mongodb_client, community_id, id, board)
        logger.info(update_result.modified_count)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_board := await retrieve_board_by_id(request.app.mongodb_client, community_id, id)
    ) is not None:
        return ResponseModel(existing_board, "Community Board updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the board data.",
    )


@router.delete("/{community_id}/id/{id}")
async def delete_board_data(request: Request, community_id: str, id: str):
    deleted_board = await delete_board(request.app.mongodb_client, community_id, id)
    if deleted_board:
        return ResponseModel(
            "Community Board with ID: {} name delete is successful".format(id),
            "Community Board name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Community Board data.",
    )

