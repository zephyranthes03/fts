import httpx
import os
from app.server.util.timelogger import time_logger
from typing import List
from app.server.util.logging import logger

# crud operations



# Add a new post into to the database
@time_logger
async def add_post(community_id:str, board_id:str, post:dict) -> dict:    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', json=post)
        data = r.json() 
        return {'post': data }
                
    return {"error": "Diagnosis couldn't be Empty."}



@time_logger
async def update_post(community_id:str, board_id:str, id:str, post:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}',
                            json=post)
        data = r.json()
        # logger.info(data)
    return data


# Retrieve all post
@time_logger
async def read_posts(community_id:str, board_id:str): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}', timeout=300)
        if len(r.json()) > 0:
            # logger.info(r.json())
            data = r.json()[0]    
    return data

# Retrieve all post by matched station ID
@time_logger
async def read_post_by_id(community_id:str, board_id:str, id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
        data["read_count"] += 1
        r = await client.put(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}',
                            json=data, timeout=300)
        data = r.json()
        # logger.info(data)
    
    return data


# Retrieve all post by matched station ID
@time_logger
async def like_post_by_id(community_id:str, board_id:str, id: str, user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
        data["like_count"] += 1
        data["like"].append(user_id)
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}', timeout=300) 
        logger.info(r.json())
    
    return data

# Retrieve all post by matched station ID
@time_logger
async def read_post_by_name(community_id:str, board_id:str, name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_POST_SERVICE")}/post/{board_id}/name/{name}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
    
    return data

# Delete a post from the database
@time_logger
async def delete_post(community_id:str, board_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_POST_SERVICE")}/post/{community_id}/{board_id}/{id}') 
    if r.status_code == 200:
        return True
    return False


