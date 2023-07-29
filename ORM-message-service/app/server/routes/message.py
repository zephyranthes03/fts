from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from fastapi.encoders import jsonable_encoder
from typing import List
# from sqlalchemy.orm import Session

from app.server.databases.message import (
    add_message,
    delete_message,
    update_message,
    retrieve_messages,
    retrieve_message_by_id,
)

from app.server.schemas.message import (
    ErrorResponseModel,
    ResponseModel,
    Message_schema,
    Update_message_schema,
)

# from app.server.databases.session import get_db


router = APIRouter()

@router.post("/{message_type}/{user_id}", response_description="Message added into the database")
async def add_message_data(request: Request, message_type: str, user_id: str, 
                           message: Message_schema = Body(...)):
    message = jsonable_encoder(message)
    if message_type:
        new_message = await add_message(request.app.mongodb_client,
                                    user_id, message)
        return ResponseModel(new_message, "Message added successfully.")
    else:
        return ErrorResponseModel(
            "An error occurred",
            status.HTTP_404_NOT_FOUND,
            f"Message type {message_type} is empty"
        )


@router.get("/{message_type}/{user_id}", response_description="Message retrieved")
async def get_messages_data(request: Request, message_type:str, user_id: str, 
                            conversation_id: str,
                          page: int = 1, size: int = 10):
    messages = await retrieve_messages(request.app.mongodb_client,
                                   user_id, conversation_id,
                                   page, size)
    messages_list = list()
    if messages:
        for message in messages:
            # message_dict = await message_list_to_dict(message)
            messages_list.append(message)
        return messages_list

    return messages

@router.get("/{message_type}/{user_id}/{id}", response_description="Message retrieved by message_id")
async def get_message_data(request: Request, message_type:str, user_id: str, 
                           id: str):
    message = await retrieve_message_by_id(request.app.mongodb_client,
                                           user_id, id)
    return message

@router.put("/{message_type}/{user_id}/{id}")
async def update_message_data(request: Request, user_id: str, id: str, req: Update_message_schema = Body(...)):
    message = {k: v for k, v in req.dict().items() if v is not None}

    if len(message) >= 1:
        update_result = await update_message(request.app.mongodb_client,
                                           user_id, id, message)
        print(update_result.modified_count,flush=True)
        if update_result.modified_count == 0:
            return ErrorResponseModel(
                "An error occurred",
                status.HTTP_404_NOT_FOUND,
                f"Message with ID {id} not found"
            )

    if (
        existing_message := await retrieve_message_by_id(request.app.mongodb_client, id)
    ) is not None:
        return ResponseModel(existing_message, "Message updated successfully.")

    return ErrorResponseModel(
        "An error occurred",
        status.HTTP_404_NOT_FOUND,
        "There was an error updating the Message data.",
    )


@router.delete("/{message_type}/{user_id}/{id}")
async def delete_message_data(request: Request, community_id: str, message_id: str, id: str):
    deleted_message = await delete_message(request.app.mongodb_client,
                                       community_id, message_id,
                                       id)
    if deleted_message:
        return ResponseModel(
            "Message with ID: {} name delete is successful".format(id),
            "Message name deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Message data.",
    )

