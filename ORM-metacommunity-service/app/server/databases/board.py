
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.board import (
    Board_schema,
    Update_board_schema,
)

# Retrieve all boards present in the database
async def retrieve_boards(mongodb_client: Optional[any], community_id:str) -> list:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    boards = list(collection.find())
    return boards


# Retrieve a board with a matching station id
async def retrieve_board_by_id(mongodb_client: Optional[any], community_id:str, id: str): # -> dict:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    board = collection.find_one(
        {"_id": id}
    )
    return board

# Retrieve a board with a matching station name
async def retrieve_board_by_name(mongodb_client: Optional[any], community_id:str, name: str): # -> dict:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    board = collection.find_one(
        {"name": name}
    )
    return board


# Add a new board into to the database
async def add_board(mongodb_client: Optional[any], community_id:str, board_data: Board_schema ) -> dict:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    new_board = collection.insert_one(board_data)
    created_board = collection.find_one(
        {"_id": new_board.inserted_id}
    )
    return created_board


# Update a board with a matching ID
async def update_board(mongodb_client: Optional[any], community_id:str, id: str, board_data: Update_board_schema) -> dict:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    update_result = collection.update_one(
        {"_id": id}, {"$set": board_data}
    )
    return update_result


# Delete a board from the database
async def delete_board(mongodb_client: Optional[any], community_id:str, id: str) -> int:
    database = mongodb_client["community_board"]
    collection = database[f"comment_{community_id}"]

    delete_result = collection.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

