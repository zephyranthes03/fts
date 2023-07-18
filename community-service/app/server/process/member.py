import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new member into to the database
async def add_member(member:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        name = member.get('disease', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                print(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/',flush=True)
                r = await client.post(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/', json=member)
                data = r.json() 
                t1_stop = process_time()
                print("Elapsed time:", t1_stop, t1_start)
                print("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
                return {'member': member['name'] }
                
            else:
                return {"error": "Diagnosis already exist!"}

        else:
            return {"error": "Diagnosis couldn't be Empty."}



async def update_member(id:str, member:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{id}',
                            json=member)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all member
async def read_members(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all member by matched station ID
async def read_member_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all member by matched station ID
async def read_member_by_name(name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a member from the database
async def delete_member(id:str):
    r = httpx.delete(f'{os.getenv("ORM_MEMBER_SERVICE")}/member/{id}') 
    if r.status_code == 200:
        return True
    return False
