import httpx
import os
from app.server.util.timelogger import time_logger
from typing import List

# crud operations



# Add a new board into to the database
@time_logger
async def add_board(community_id:str, board_id:str, board:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', json=board)
        data = r.json() 
        return {'board': board['name'] }
                
    return {"error": "Diagnosis couldn't be Empty."}



@time_logger
async def update_board(community_id:str, board_id:str, id:str, board:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}',
                            json=board)
        data = r.json()
        print(data,flush=True)
    return data


# Retrieve all board
@time_logger
async def read_boards(community_id:str, board_id:str): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]    
    return data

# Retrieve all board by matched station ID
@time_logger
async def read_board_by_id(community_id:str, board_id:str, id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()
        data["read_count"] += 1
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)    
    return data


# Retrieve all board by matched station ID
@time_logger
async def read_board_by_name(community_id:str, board_id:str, name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{board_id}/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()
    
    return data

# Delete a board from the database
@time_logger
async def delete_board(community_id:str, board_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}') 
    if r.status_code == 200:
        return True
    return False


