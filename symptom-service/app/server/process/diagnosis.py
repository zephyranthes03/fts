import httpx
import os
from typing import List
from app.server.util.timelogger import time_logger
# crud operations
from app.server.util.logging import logger

@time_logger
# Add a new diagnosis into to the database
async def add_diagnosis(diagnosis:dict) -> dict:
    async with httpx.AsyncClient() as client:
        name = diagnosis.get('disease', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                logger.info(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/')
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/', json=diagnosis)
                data = r.json() 
                return {'diagnosis': diagnosis['diagnosis'] }
                
            else:
                return {"error": "Diagnosis already exist!"}

        else:
            return {"error": "Diagnosis couldn't be Empty."}



@time_logger
async def update_diagnosis(id:str, diagnosis:dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/id/{id}',
                            json=diagnosis)
        data = r.json()
        logger.info(data)
    return data


@time_logger
# Retrieve all diagnosis
async def read_diagnosises(): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/', timeout=300)
        if len(r.json()) > 0:
            logger.info(r.json())
            data = r.json()[0]    
    return data

@time_logger
# Retrieve all diagnosis by matched station ID
async def read_diagnosis_by_id(id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/id/{id}', timeout=300) 
        logger.info(r.json())
        data = r.json()    
    return data


@time_logger
# Retrieve all diagnosis by matched station ID
async def read_diagnosis_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/name/{name}', timeout=300) 
        logger.info(r.json())

        data = r.json()    
    return data

@time_logger
# Delete a diagnosis from the database
async def delete_diagnosis(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/diagnosis/id/{id}') 
    if r.status_code == 200:
        return True
    return False
