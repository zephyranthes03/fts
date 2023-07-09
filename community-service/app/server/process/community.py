import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new community into to the database
async def add_community(community:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        name = community.get('disease', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                print(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/',flush=True)
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/', json=community)
                data = r.json() 
                t1_stop = process_time()
                print("Elapsed time:", t1_stop, t1_start) 
                print("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
                return {'community': community['community'] }
                
            else:
                return {"error": "Diagnosis already exist!"}

        else:
            return {"error": "Diagnosis couldn't be Empty."}



async def update_community(id:str, community:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/{id}',
                            json=community)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all community
async def read_Communities(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all community by matched station ID
async def read_community_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all community by matched station ID
async def read_community_by_name(name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a community from the database
async def delete_community(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/community/{id}') 
    if r.status_code == 200:
        return True
    return False
