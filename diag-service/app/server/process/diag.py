import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new diag into to the database
async def add_diag(diag:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM-DIAG-SERVICE")}/diag/',
                            json=diag)
        data = r.json() 
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return {'id': diag['id'] }

async def update_diag(id:str, diag:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM-DIAG-SERVICE")}/diag/{id}',
                            json=diag)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all diag
async def read_diags(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM-DIAG-SERVICE")}/diag/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all diag by matched station ID
async def read_diag_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM-DIAG-SERVICE")}/diag/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Delete a diag from the database
async def delete_diag(id:str):
    r = httpx.delete(f'{os.getenv("ORM-DIAG-SERVICE")}/diag/{id}') 
    if r.status_code == 200:
        return True
    return False
