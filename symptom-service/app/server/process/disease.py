import httpx
import os
from typing import List
from app.server.util.timelogger import time_logger
from app.server.util.logging import logger

# crud operations


# Add a new disease into to the database
@time_logger
async def add_disease(disease:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        name = disease.get('disease', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/name/{name}')
            logger.info(r)
            data = r.json()
            logger.info(data)
            if data is None:

                logger.info(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/')
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/', json=disease)
                data = r.json() 
                return {'disease': disease['disease'] }
                
            else:
                return {"error": "Disease already exist!"}

        else:
            return {"error": "Disease couldn't be Empty."}



@time_logger
async def update_disease(id:str, disease:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/id/{id}',
                            json=disease)
        data = r.json()
        logger.info(data)
    return data


# Retrieve all disease
async def read_diseases(): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/', timeout=300)
        logger.info(r.json())
        if len(r.json()) > 0:
            data = r.json()[0]
    
    return data

# Retrieve all disease by matched station ID
@time_logger
async def read_disease_by_id(id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/id/{id}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
    
    return data

# Retrieve all disease by matched station ID
@time_logger
async def read_disease_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/name/{name}', timeout=300) 
        # logger.info(r.json())

        data = r.json()
    
    return data

# Delete a disease from the database
@time_logger
async def delete_disease(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/disease/id/{id}') 
    if r.status_code == 200:
        return True
    return False
