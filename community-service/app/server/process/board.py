import httpx
import os
from time import process_time
from typing import List

# crud operations



# Add a new board into to the database
async def add_board(community_id:str, board_id:str, board:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}', json=board)
        data = r.json() 
        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)
        return {'board': board['name'] }
                
    return {"error": "Diagnosis couldn't be Empty."}



async def update_board(community_id:str, board_id:str, id:str, board:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}/{id}',
                            json=board)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all board
async def read_boards(community_id:str, board_id:str): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all board by matched station ID
async def read_board_by_id(community_id:str, board_id:str, id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()
        data["read_count"] += 1
        r = await client.get(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all board by matched station ID
async def read_board_by_name(community_id:str, board_id:str, name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{board_id}/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a board from the database
async def delete_board(community_id:str, board_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_BOARD_SERVICE")}/board/{community_id}/{board_id}/{id}') 
    if r.status_code == 200:
        return True
    return False


