import httpx
import os
from app.server.util.timelogger import time_logger
from typing import List
from app.server.util.logging import logger

# crud operations



# Add a new member into to the database
@time_logger
async def add_member(community_id:str, member:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}', json=member)
        data = r.json() 
        return {'member': member['name'] }
                
    return {"error": "Diagnosis couldn't be Empty."}



@time_logger
async def update_member(community_id:str, id:str, member:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}/id/{id}',
                            json=member)
        data = r.json()
        logger.info(data)
    return data


# Retrieve all member
@time_logger
async def read_members(community_id:str): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}', timeout=300)
        if len(r.json()) > 0:
            # logger.info(r.json())
            data = r.json()[0]    
    return data

# Retrieve all member by matched station ID
@time_logger
async def read_member_by_id(community_id:str, id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}/id/{id}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
    return data


# Retrieve all member by matched station ID
@time_logger
async def read_member_by_name(community_id:str, name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}/name/{name}', timeout=300) 
        # logger.info(r.json())

        data = r.json()

    return data

# Delete a member from the database
@time_logger
async def delete_member(community_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}/id{id}') 
    if r.status_code == 200:
        return True
    return False


# Delete a member from the database
async def delete_member(community_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{community_id}/id/{id}') 
    if r.status_code == 200:
        return True
    return False