
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.board import (
    Board_schema,
    Update_board_schema,
)

# Retrieve all boards present in the database
async def retrieve_boards(database: Optional[any]) -> list:
    boards = list(database.find())
    return boards


# Retrieve a board with a matching station id
async def retrieve_board_by_id(database: Optional[any], id: str): # -> dict:
    board = database.find_one(
        {"_id": id}
    )
    return board
    
# Add a new board into to the database
async def add_board(database: Optional[any], board_data: Board_schema ) -> dict:
    new_board = database.insert_one(board_data)
    created_board = database.find_one(
        {"_id": new_board.inserted_id}
    )
    return created_board


# Update a board with a matching ID
async def update_board(database: Optional[any], id: str, board_data: Update_board_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": board_data}
    )
    return update_result


# Delete a board from the database
async def delete_board(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

