from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.databases.llm_result import (
    add_llm_result,
    delete_llm_result,
    update_llm_result,
    retrieve_llm_results,
    retrieve_llm_results_to_feedback,
    retrieve_llm_result_by_id,
    retrieve_llm_result_by_name
)
from app.server.schemas.llm_result import (
    ErrorResponseModel,
    ResponseModel,
    Llm_result_schema,
    Update_llm_result_schema,
)

router = APIRouter()


@router.post("/", response_description="Llm_result data added into the database")
async def add_llm_result_data(request: Request, llm_result: Llm_result_schema = Body(...)):
    llm_result = jsonable_encoder(llm_result)
    new_llm_result = await add_llm_result(request.app.database['llm_results'], llm_result)
    return ResponseModel(new_llm_result, "Llm_result added successfully.")

@router.get("/", response_description="llm_result retrieved")
async def get_llm_results_data(request: Request):
    llm_results = await retrieve_llm_results(request.app.database['llm_results'])
    llm_results_list = list()
    if llm_results:
        for llm_result in llm_results:
            # llm_result_dict = await llm_result_list_to_dict(llm_result)
            llm_results_list.append(llm_result)
        return llm_results_list

    return llm_results

@router.get("/feedback/{type}", response_description="llm_result retrieved for PEFT")
async def get_llm_results_data(request: Request, type:str):
    llm_results = await retrieve_llm_results_to_feedback(request.app.database['llm_results'], type)
    llm_results_list = list()
    if llm_results:
        for llm_result in llm_results:
            # llm_result_dict = await llm_result_list_to_dict(llm_result)
            llm_results_list.append(llm_result)
        return llm_results_list

    return llm_results


@router.get("/id/{id}", response_description="Llm_result data retrieved by llm_result_id")
async def get_llm_result_data_by_id(request: Request, id: str):
    llm_result = await retrieve_llm_result_by_id(request.app.database['llm_results'], id)
    return llm_result

@router.get("/name/{name}", response_description="Llm_result data retrieved by llm_result name")
async def get_llm_result_data_by_name(request: Request, name: str):
    llm_result = await retrieve_llm_result_by_name(request.app.database['llm_results'], name)
    return llm_result

@router.put("/{id}")
async def update_llm_result_data(request: Request, id: str, req: Update_llm_result_schema = Body(...)):
    llm_result = {k: v for k, v in req.dict().items() if v is not None}

    if len(llm_result) >= 1:
        update_result = await update_llm_result(request.app.database["llm_results"], id, llm_result)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Book with ID {id} not found"
            )

    if (
        existing_llm_result := await retrieve_llm_result_by_id(request.app.database['llm_results'], id)
    ) is not None:
        return ResponseModel(existing_llm_result, "Llm_result updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the llm_result data.",
    )


@router.delete("/{id}")
async def delete_llm_result_data(request: Request, id: str):
    deleted_llm_result = await delete_llm_result(request.app.database['llm_results'], id)
    if deleted_llm_result:
        return ResponseModel(
            "Llm_result with ID: {} name delete is successful".format(id),
            "Llm_result name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Llm_result data.",
    )

