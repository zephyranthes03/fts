import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new disease into to the database
async def add_disease(disease:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM-DIAG-SERVICE")}/disease/',
                            json=disease)
        data = r.json() 
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return {'id': disease['id'] }

async def update_disease(id:str, disease:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM-DIAG-SERVICE")}/disease/{id}',
                            json=disease)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all disease
async def read_diseases(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM-DIAG-SERVICE")}/disease/', timeout=300)
        print(r.json(),flush=True)
        if len(r.json()['data']) > 0:
            data = r.json()['data'][0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all disease by matched station ID
async def read_disease_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM-DIAG-SERVICE")}/disease/{id}', timeout=300) 
        print(r.json()['data'],flush=True)

        data = r.json()['data']

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Delete a disease from the database
async def delete_disease(id:str):
    r = httpx.delete(f'{os.getenv("ORM-DIAG-SERVICE")}/disease/{id}') 
    if r.status_code == 200:
        return True
    return False
