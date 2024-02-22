import httpx
import os
from typing import List
from timelogger import time_logger
# crud operations



# Add a new application into to the database
@time_logger
async def add_application(community_id:str, application:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}', json=application)
        data = r.json() 
        return {'application': application }
                
    return {"error": "Diagnosis couldn't be Empty."}



@time_logger
async def update_application(community_id:str, id:str, application:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/{id}',
                            json=application)
        data = r.json()
        print(data,flush=True)
    return data


# Retrieve all application
@time_logger
async def read_applications(community_id:str): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]    
    return data

# Retrieve all application by matched station ID
@time_logger
async def read_application_by_id(community_id:str, id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/id/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()    
    return data


# Retrieve all application by matched station ID
async def read_application_by_name(community_id:str, name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()    
    return data

# Delete a application from the database
@time_logger
async def delete_application(community_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/id/{id}') 
    if r.status_code == 200:
        return True
    return False


# Delete a application from the database
async def join_request(community_id:str, member_id:str, invitation_message:str):
    pass

# Delete a application from the database
async def join_response(community_id:str, member_id:str, invitation_message:str):
    pass


# Delete a application from the database
async def join_invitation(community_id:str, member_id:str, request_form:dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/request/{member_id}', json=request_form)
        data = r.json() 
        return {'application': member_id }
                
    return {"error": "Diagnosis couldn't be Empty."}

