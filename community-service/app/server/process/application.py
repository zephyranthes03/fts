import httpx
import os
from time import process_time
from typing import List

# crud operations



# Add a new application into to the database
async def add_application(community_id:str, application:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/{community_id}/application/', json=application)
        data = r.json() 
        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)
        return {'application': application['name'] }
                
    return {"error": "Diagnosis couldn't be Empty."}



async def update_application(community_id:str, id:str, application:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_MEMBER_SERVICE")}/{community_id}/application/{id}',
                            json=application)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all application
async def read_applications(community_id:str): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/{community_id}/application/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all application by matched station ID
async def read_application_by_id(community_id:str, id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all application by matched station ID
async def read_application_by_name(community_id:str, name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a application from the database
async def delete_application(community_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/{id}') 
    if r.status_code == 200:
        return True
    return False


# Delete a application from the database
async def delete_application(community_id:str, id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/application/{community_id}/{id}') 
    if r.status_code == 200:
        return True
    return False

# Delete a application from the database
async def join_invitation(community_id:str, member_id:str, invitation_message:str):
    pass

# Delete a application from the database
async def join_request(community_id:str, member_id:str, request_form:dict):
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/{community_id}/application/{member_id}', json=request_form)
        data = r.json() 
        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)
        return {'application': member_id }
                
    return {"error": "Diagnosis couldn't be Empty."}

# Delete a application from the database
async def join_response(community_id:str, member_id:str, invitation_message:str):
    pass
