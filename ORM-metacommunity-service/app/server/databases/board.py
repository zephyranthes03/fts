
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.config.config import settings

from app.server.schemas.board import (
    Board_schema,
    Update_board_schema,
)


from app.server.databases.community import (
    update_community,
    retrieve_community_by_id
)

# Retrieve all boards present in the database
async def retrieve_boards(mongodb_client: Optional[any], community_id:str) -> list:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    boards = list(collection_board.find())
    return boards


# Retrieve a board with a matching station id
async def retrieve_board_by_id(mongodb_client: Optional[any], community_id:str, id: str): # -> dict:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    board = collection_board.find_one(
        {"_id": id}
    )
    return board

# Retrieve a board with a matching station name
async def retrieve_board_by_name(mongodb_client: Optional[any], community_id:str, name: str): # -> dict:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    board = collection_board.find_one(
        {"name": name}
    )
    return board


# Add a new board into to the database
async def add_board(mongodb_client: Optional[any], community_id:str, board_data: Board_schema ) -> dict:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    database_community = mongodb_client[settings.DATABASE_METACOMMUNITY]
    collection_community = database_community[settings.DATABASE_METACOMMUNITY]

    new_board = collection_board.insert_one(board_data)
    created_board = collection_board.find_one(
        {"_id": new_board.inserted_id}
    )

    community_data = await retrieve_community_by_id(mongodb_client, community_id)

    community_data["boards"].append({"id": created_board["_id"], 
                                     "kind": created_board["kind"], 
                                     "name": created_board["name"]})

    update_result = await update_community(mongodb_client, community_id, community_data)
    # print(update_result.modified_count,flush=True)

    return created_board


# Update a board with a matching ID
async def update_board(mongodb_client: Optional[any], community_id:str, id: str, board_data: Update_board_schema) -> dict:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    update_result = collection_board.update_one(
        {"_id": id}, {"$set": board_data}
    )

    ### TODO board + community part

    community_data = await retrieve_community_by_id(mongodb_client, community_id)

    boards = community_data["boards"]
    # find_updated_boards =  list(filter(lambda boards: boards['id'] == id, boards))
    # board_index = boards.index(find_updated_boards[0])

    board_index = [i for i,_ in enumerate(boards) if _['id'] == id][0]

    community_data["boards"][board_index] = {"id": boards[board_index]["id"], 
                                     "kind": board_data["kind"], 
                                     "name": board_data["name"]}

    update_community_result = await update_community(mongodb_client, community_id, community_data)

    return update_result


# Delete a board from the database
async def delete_board(mongodb_client: Optional[any], community_id:str, id: str) -> int:
    database_board = mongodb_client[settings.DATABASE_BOARD]
    collection_board = database_board[f"board_{community_id}"]

    delete_result = collection_board.delete_one({"_id": id})

    community_data = await retrieve_community_by_id(mongodb_client, community_id)

    boards = community_data["boards"]
    board_index = [i for i,_ in enumerate(boards) if _['id'] == id][0]

    del community_data["boards"][board_index]

    update_community_result = await update_community(mongodb_client, community_id, community_data)

    return delete_result

