import httpx
import os
from time import process_time
from typing import List

# crud operations



# Add a new post into to the database
async def add_post(community_id:str, board_id:str, post:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', json=post)
        data = r.json() 
        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)
        return {'post': data }
                
    return {"error": "Diagnosis couldn't be Empty."}



async def update_post(community_id:str, board_id:str, id:str, post:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}',
                            json=post)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all post
async def read_posts(community_id:str, board_id:str): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all post by matched station ID
async def read_post_by_id(community_id:str, board_id:str, id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()
        data["read_count"] += 1
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all post by matched station ID
async def like_post_by_id(community_id:str, board_id:str, id: str, user_id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()
        data["like_count"] += 1
        data["like"].append(user_id)
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Retrieve all post by matched station ID
async def read_post_by_name(community_id:str, board_id:str, name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{board_id}/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a post from the database
async def delete_post(community_id:str, board_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}') 
    if r.status_code == 200:
        return True
    return False


