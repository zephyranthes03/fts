import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new symptom into to the database
async def add_symptom_index(symptom_index:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/',
                            json=symptom_index)
        data = r.json() 
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return {'id': symptom_index['id'] }

async def update_symptom_index(id:str, symptom_index:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}',
                            json=symptom_index)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all symptom
async def read_symptom_indexes(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all symptom_index by matched station ID
async def read_symptom_index_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Delete a symptom from the database
async def delete_symptom_index(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}') 
    if r.status_code == 200:
        return True
    return False
