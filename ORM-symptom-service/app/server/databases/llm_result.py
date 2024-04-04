
from datetime import datetime

from typing import List, Optional

# import databases
# from fastapi import FastAPI

from app.server.schemas.llm_result import (
    Llm_result_schema,
    Update_llm_result_schema,
)

# Retrieve all llm_results present in the database
async def retrieve_llm_results(database: Optional[any]) -> list:
    llm_results = list(database.find())
    return llm_results


# Retrieve a llm_result with a matching station id
async def retrieve_llm_result_by_id(database: Optional[any], id: str): # -> dict:
    llm_result = database.find_one(
        {"_id": id}
    )
    return llm_result

# Retrieve a llm_result with a matching station id
async def retrieve_llm_result_by_name(database: Optional[any], name: str): # -> dict:
    llm_result = database.find_one(
        {"llm_result": name}
    )
    return llm_result
    
# Add a new llm_result into to the database
async def add_llm_result(database: Optional[any], llm_result_data: Llm_result_schema ) -> dict:
    new_llm_result = database.insert_one(llm_result_data)
    created_llm_result = database.find_one(
        {"_id": new_llm_result.inserted_id}
    )
    return created_llm_result


# Update a llm_result with a matching ID
async def update_llm_result(database: Optional[any], id: str, llm_result_data: Update_llm_result_schema) -> dict:
    update_result = database.update_one(
        {"_id": id}, {"$set": llm_result_data}
    )
    return update_result


# Delete a llm_result from the database
async def delete_llm_result(database: Optional[any], id: str) -> int:
    delete_result = database.delete_one({"_id": id})
    print(delete_result,flush=True)
    return delete_result

