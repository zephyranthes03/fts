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

from app.server.process.board import (
    read_board_by_id,
    read_board_by_name,
    read_boards,
    add_board,
    delete_board,
    update_board,
)

from app.server.schemas.board import (
    ErrorResponseModel,
    ResponseModel,
    Board_schema,
    Update_board_schema
)


router = APIRouter()



@router.post("/{community_id}/board/{board_id}", response_description="Board data folder added into the database")
async def add_board_data(community_id:str, board_id:str, board: Board_schema = Body(...), dependencies:dict=Depends(verify_token)):
    board = jsonable_encoder(board)
    new_board = await add_board(community_id, board_id, board)
    if new_board.get('error', None):
        return ErrorResponseModel(
            new_board.get('error', None),
            500,
            new_board.get('message', None)
        )
    return ResponseModel(new_board, "Board added successfully.")

@router.get("/{community_id}/board/{board_id}", response_description="Communites retrieved")
async def get_boards(community_id:str, board_id:str, dependencies:dict=Depends(verify_token)):
    boards = await read_boards(community_id, board_id)
    if boards:
        return ResponseModel(boards, "Communites data statistic retrieved successfully")
    return ResponseModel(boards, "Empty list returned")

@router.get("/{community_id}/board/{board_id}/id/{id}", response_description="Communites retrieved")
async def get_board_by_id(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    boards = await read_board_by_id(community_id, board_id, id)
    if boards:
        return ResponseModel(boards, "Communites data statistic retrieved successfully")
    return ResponseModel(boards, "Empty list returned")

@router.get("/{community_id}/board/{board_id}/name/{name}", response_description="Communites retrieved")
async def get_board_by_name(community_id:str, board_id:str, name:str, dependencies:dict=Depends(verify_token)):
    boards = await read_board_by_name(community_id, board_id, name)
    if boards:
        return ResponseModel(boards, "Communites data statistic retrieved successfully")
    return ResponseModel(boards, "Empty list returned")

@router.put("/{community_id}/board/{board_id}/id/{id}")
async def update_board_data(community_id:str, board_id:str, id: str, req: Update_board_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    board = jsonable_encoder(req)
    updated_board = await update_board(community_id, board_id, id, board)
    if 'data' in updated_board:
        return ResponseModel(
            "Board with ID: {} name update is successful".format(id),
            "Board name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the board data.",
    )

@router.delete("/{community_id}/board/{board_id}/id/{id}", response_description="Board data deleted from the database")
async def delete_board_data(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_board = await delete_board(community_id, board_id, id)
    if deleted_board == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )
