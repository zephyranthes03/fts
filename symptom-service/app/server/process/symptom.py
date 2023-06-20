import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new symptom into to the database
async def add_symptom(symptom:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom/',
                            json=symptom)
        data = r.json() 
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return {'id': symptom['id'] }

async def update_symptom(id:str, symptom:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom/{id}',
                            json=symptom)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all symptom
async def read_symptoms(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all symptom by matched station ID
async def read_symptom_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Delete a symptom from the database
async def delete_symptom(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom/{id}') 
    if r.status_code == 200:
        return True
    return False
