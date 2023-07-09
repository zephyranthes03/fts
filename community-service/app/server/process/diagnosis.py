import httpx
import os
from time import process_time
from typing import List

# crud operations


# Add a new diagnosis into to the database
async def add_diagnosis(diagnosis:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        name = diagnosis.get('disease', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                print(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/',flush=True)
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/', json=diagnosis)
                data = r.json() 
                t1_stop = process_time()
                print("Elapsed time:", t1_stop, t1_start) 
                print("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
                return {'diagnosis': diagnosis['diagnosis'] }
                
            else:
                return {"error": "Diagnosis already exist!"}

        else:
            return {"error": "Diagnosis couldn't be Empty."}



async def update_diagnosis(id:str, diagnosis:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/{id}',
                            json=diagnosis)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all diagnosis
async def read_diagnosises(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all diagnosis by matched station ID
async def read_diagnosis_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all diagnosis by matched station ID
async def read_diagnosis_by_name(name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Delete a diagnosis from the database
async def delete_diagnosis(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/{id}') 
    if r.status_code == 200:
        return True
    return False
