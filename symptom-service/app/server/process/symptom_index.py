import httpx
import os
import base64
from time import process_time
from typing import List
from app.server.util.symptom import extract_symptom

# crud operations

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")


async def llm_diagnosis(image_base64: base64, query_text: str, email: str):

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
            "text": query_text
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
    "max_tokens": 300
    }
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(timeout=120.0)
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
    return result

# Add a new symptom into to the database
async def add_symptom_index(symptom_index:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        name = symptom_index.get('symptom_index', None)
        if name:
            r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/name/{name}')
            data = r.json() 
            if data.get('detail', 'Failure') == 'Not Found':

                print(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/',flush=True)
                r = await client.post(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/', json=symptom_index)
                data = r.json() 
                t1_stop = process_time()
                print("Elapsed time:", t1_stop, t1_start) 
                print("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
                return {'symptom_index': symptom_index['symptom_index'] }
                
            else:
                return {"error": "Symptom_index already exist!"}

        else:
            return {"error": "Symptom_index couldn't be Empty."}



async def update_symptom_index(id:str, symptom_index:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}',
                            json=symptom_index)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all symptom
async def read_symptom_indexes(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/', timeout=300)
        if len(r.json()) > 0:
            print(r.json(),flush=True)
            data = r.json()[0]

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start) 
    
    return data

# Retrieve all symptom_index by matched ID
async def read_symptom_index_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/id/{id}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Retrieve all symptom_index by matched symptom
async def read_symptom_index_by_name(name: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/name/{name}', timeout=300) 
        print(r.json(),flush=True)

        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data




# Delete a symptom from the database
async def delete_symptom_index(id:str):
    r = httpx.delete(f'{os.getenv("ORM_SYMPTOM_SERVICE")}/symptom_index/{id}') 
    if r.status_code == 200:
        return True
    return False
