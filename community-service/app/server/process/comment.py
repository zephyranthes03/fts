import httpx
import os
from time import process_time
from typing import List

# crud operations



# Add a new comment into to the database
async def add_comment(community_id:str, board_id:str, post_id:str, comment:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}', json=comment)
        data = r.json() 
        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)
        return {'comment': data['data'] }
                
    return {"error": "Comment couldn't be Empty."}



async def update_comment(community_id:str, board_id:str, post_id:str, id:str, comment:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}/id/{id}',
                            json=comment)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all comment
async def read_comments(community_id:str, board_id:str, post_id:str): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}', timeout=300)
        print(r,flush=True)
        print(r.json(),flush=True)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
            return data
    return {"error": "Comment is Empty."}

# Retrieve all comment by matched station ID
async def read_comment_by_id(community_id:str, board_id:str, post_id:str, id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}/id/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all comment by matched station ID
async def read_comment_by_name(community_id:str, board_id:str, post_id:str, name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a comment from the database
async def delete_comment(community_id:str, board_id:str, post_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_COMMENT_SERVICE")}/comment/{community_id}/{board_id}/post/{post_id}/id/{id}') 
    if r.status_code == 200:
        return True
    return False

