
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.community_board import (
    Community_board_schema,
    Update_community_board_schema,
)

# Retrieve all boards present in the database
async def retrieve_community_boards(database: Optional[any]) -> list:
    community_boards = list(database.find())
    return community_boards


# Retrieve a board with a matching station id
async def retrieve_community_board_by_id(database: Optional[any], id: str): # -> dict:
    community_board = database.find_one(
        {"_id": id}
    )
    return community_board

# Retrieve a board with a matching station name
async def retrieve_community_board_by_name(database: Optional[any], name: str): # -> dict:
    community_board = database.find_one(
        {"name": name}
    )
    return community_board


# Add a new board into to the database
async def add_community_board(database: Optional[any], community_board_data: Community_board_schema ) -> dict:
    new_community_board = database.insert_one(community_board_data)
    created_community_board = database.find_one(
        {"_id": new_community_board.inserted_id}
    )
    return created_community_board


# Update a board with a matching ID
async def update_community_board(database: Optional[any], id: str, community_board_data: Update_community_board_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": community_board_data}
    )
    return update_result


# Delete a board from the database
async def delete_community_board(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

