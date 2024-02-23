import httpx
import os
from app.server.util.timelogger import time_logger
from typing import List

# crud operations


# Add a new community into to the database
@time_logger
async def add_community(community:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        name = community.get('name', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/name/{name}')
            data = r.json() 

            if data is None or (data and data.get('detail', 'Failure') == 'Not Found'):

                print(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/',flush=True)
                r = await client.post(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/', json=community)
                data = r.json() 
                return {'community': community['name'] }
                
            else:
                return {"error": "Community name is already exist!"}

        else:
            return {"error": "Community name couldn't be Empty."}



@time_logger
async def update_community(id:str, community:dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/{id}',
                            json=community)
        data = r.json()
        print(data,flush=True)
    return data


# Retrieve all community
@time_logger
async def read_communities(): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/', timeout=300)
        if len(r.json()) > 0:
            # print(r.json(),flush=True)
            data = r.json()[0]    
    return data

# Retrieve all community by matched station ID
@time_logger
async def read_community_by_id(id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/{id}', timeout=300) 
        print(r.json(),flush=True)
        data = r.json()    
    return data


# Retrieve all community by matched station ID
@time_logger
async def read_community_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()    
    return data

# Delete a community from the database
@time_logger
async def delete_community(id:str):
    r = httpx.delete(f'{os.getenv("ORM_METACOMMUNITY_SERVICE")}/community/{id}') 
    if r.status_code == 200:
        return True
    return False
