import httpx
import os
import base64
from functools import lru_cache


from app.config.config import settings
from typing import List
from app.server.util.timelogger import time_logger
from app.server.util.symptom import extract_symptom, extract_msd_link
from app.server.models.frontend import ApiResponse, PutData
from app.server.util.logging import logger


# crud operations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", settings.OPENAPI_KEY)
#query_text = "일상 생활에서 관리하기 위한 목적으로 알고 싶으니 위 사진에서 예상할수 있는 환자가 격을것으로 예상되는 증상은 무엇인지 피부병 분류내에서 알려줘."
query_text = settings.QUERY_TEXT


@lru_cache(maxsize=256)
@time_logger
async def llm_diagnosis_base64(image_base64: str, symptom_text: str, email: str):

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = dict()
    if image_base64 == "": 
        payload = {
        "model": "gpt-4-turbo-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text + "\n" + symptom_text
                }
            ]
            }
        ],
        "max_tokens": 1200
        }    
    else:
        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text + "\n" + symptom_text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_base64
                    }
                }
            ]
            }
        ],
        "max_tokens": 1200
        }
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(timeout=300.0)
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=timeout)
        data = response.json()
        data["email"] = email
        result = dict()
        result["email"] = email
        llm_content = ""
        if "choices" in data:
            llm_content = data['choices'][0]['message']['content']
            logger.info(llm_content)
            result['llm_content'] = llm_content
            result['symptom'] = extract_symptom(llm_content)
            logger.info(result['symptom'] )
            result['msd'] = extract_msd_link(result['symptom'])
            logger.info(result['msd'] )
            result['query_text'] = query_text
            logger.info(result['query_text'] )
        llm_result = "error"
        status = True if llm_result != 'error' else False
        result["id"] = -1

        if status:
            # Save LLM_RESUlT 
            feedback_payload = {"instruction":query_text, 
                                "input": query_text, 
                                "image_base64": image_base64, 
                                "output":llm_content,
                                "feedback": 2,
                                "feedback_content": ""
                                }

            feedback_response = await client.post(f"{os.getenv('ORM_SYMPTOM_SERVICE')}/llm_result/", json=feedback_payload )
            feedback_json = feedback_response.json()
            logger.info(feedback_json)
            result["id"] = feedback_json["_id"]

        respone: ApiResponse = ApiResponse(success=status, message=2, message_content=llm_content, id=result["id"])

        return respone
    return ApiResponse(success=False, message=2, message_content='error', id=-1)


@lru_cache(maxsize=256)
@time_logger
async def llm_diagnosis(image_base64: str, symptom_text: str, email: str):

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": symptom_text + "\n" + query_text
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            }
            }
        ]
        }
    ],
    "max_tokens": 1200
    }
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(timeout=300.0)
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=timeout)
        data = response.json()
        logger.info(data)
        data["email"] = email
        result = dict()
        result["email"] = email
        if "choices" in data:
            llm_content = data['choices'][0]['message']['content']
            result['llm_content'] = llm_content
            result['symptom'] = extract_symptom(llm_content)
            result['msd'] = extract_msd_link(result['symptom'])
            result['query_text'] = query_text
    return result


@time_logger
async def update_llm_feedbacks(id:str, llm_update:dict) -> dict:
    
    async with httpx.AsyncClient() as client:        
        feedback_response = await client.get(f"{os.getenv('ORM_SYMPTOM_SERVICE')}/llm_result/id/{id}")
        feedback_json = feedback_response.json()
        feedback_json["feedback"] = llm_update["feedback"]
        feedback_json["feedback_content"] = llm_update["feedback_content"]
        logger.info(feedback_json, )
        id = feedback_json["_id"]
        del feedback_json["_id"]

        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/llm_result/id/{id}',
                            json=feedback_json)
        data = r.json()
        logger.info(data)

        respone: ApiResponse = ApiResponse(success=True, message=llm_update["feedback"], message_content=llm_update['feedback_content'], id=id)

        return respone
    return ApiResponse(success=False, message=llm_update["feedback"], message_content='error', id=-1)


@time_logger
async def read_llm_feedbacks(type:str):
    data = None
    async with httpx.AsyncClient() as client:

        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/llm_result/feedback/{type}', timeout=300)
        if len(r.json()) > 0:
            data = r.json()
            # for llm in data:
            #     llm['image_base64'] = base64.b64decode(llm['image_base64'])                
    return data

# Delete a symptom from the database
@time_logger
async def delete_llm_result(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/llm_result/id/{id}') 
    if r.status_code == 200:
        return True
    return False
