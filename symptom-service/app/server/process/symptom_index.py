import httpx
import os
import base64
from functools import lru_cache


from app.config.config import settings
from typing import List
from app.server.util.timelogger import time_logger
from app.server.util.symptom import extract_symptom, extract_msd_link

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
        print(data,flush=True)
        data["email"] = email
        result = dict()
        result["email"] = email
        llm_content = ""
        if "choices" in data:
            llm_content = data['choices'][0]['message']['content']
            print(llm_content,flush=True)
            result['llm_content'] = llm_content
            result['symptom'] = extract_symptom(llm_content)
            print(result['symptom'] ,flush=True)
            result['msd'] = extract_msd_link(result['symptom'])
            print(result['msd'] ,flush=True)
            result['query_text'] = query_text
            print(result['query_text'] ,flush=True)


        # Save LLM_RESUlT 
        feedback_payload = {"instruction":query_text, 
                            "input": query_text, 
                            "image_base64": image_base64, 
                            "output":llm_content,
                            "feedback": 2,
                            "feedback_content": ""
                            }

        feedback_response = await client.post(f"{os.getenv('ORM_SYMPTOM_SERVICE')}/llm_result", json=feedback_payload )
        feedback_json = feedback_response
        print(feedback_json,flush=True)
    return result


@time_logger
async def feedback_update(feedback_id: str, feedback: int, feedback_content: str):
    async with httpx.AsyncClient() as client:
        # Save LLM_RESUlT 
        feedback_response = await client.get(f"{os.getenv('ORM_SYMPTOM_SERVICE')}/symptom/feedback/{feedback_id}")
        feedback_json = feedback_response.json()
        feedback_json["feedback"] = feedback
        feedback_json["feedback_content"] = feedback_content
        print(feedback_json, flush=True)
        del feedback_json["_id"]
        feedback_response = await client.put(f"{os.getenv('ORM_SYMPTOM_SERVICE')}/symptom/", json=feedback_json )
        feedback_data = feedback_response.json()
        print(feedback_data,flush=True)    

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
        print(data,flush=True)
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
# Add a new symptom into to the database
async def add_symptom_index(symptom_index:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        name = symptom_index.get('symptom_index', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                print(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/',flush=True)
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/', json=symptom_index)
                data = r.json() 
                return {'symptom_index': symptom_index['symptom_index'] }
                
            else:
                return {"error": "Symptom_index already exist!"}

        else:
            return {"error": "Symptom_index couldn't be Empty."}



@time_logger
async def update_symptom_index(id:str, symptom_index:dict) -> dict:
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}',
                            json=symptom_index)
        data = r.json()
        print(data,flush=True)
    return data

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

# Retrieve all symptom
@time_logger
async def read_symptom_indexes(): # -> dict:
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]
    
    return data

@time_logger
# Retrieve all symptom_index by matched ID
async def read_symptom_index_by_id(id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/id/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()    
    return data

# Retrieve all symptom_index by matched symptom
@time_logger
async def read_symptom_index_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

    return data




# Delete a symptom from the database
@time_logger
async def delete_symptom_index(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}') 
    if r.status_code == 200:
        return True
    return False
