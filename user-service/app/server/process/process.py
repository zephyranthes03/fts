import httpx
import os
from time import process_time
from typing import List
from fastapi.responses import JSONResponse

# crud operations


# Add a new user into to the database
async def add_user(user:dict) -> dict:
    t1_start = process_time()
    
    async with httpx.AsyncClient() as client:

        email = user.get('email', None)
        if email:
            r = await client.get(f'{os.getenv("ORM_USER_SERVICE")}/user/email/{email}')
            data = r.json() 
            # print(data,flush=True)
            # print(data.get("email",None),flush=True)
            if data.get("email", None) is None:
                print(f'{os.getenv("ORM_USER_SERVICE")}/user/',flush=True)
                r = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/', json=user)
                data = r.json() 
                t1_stop = process_time()
                print("Elapsed time:", t1_stop, t1_start) 
                print("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
                return {'email':user.get('email')}

            else:
                return {"error": "Email already exist!"}

        else:
            return {"error": "Email couldn't be Empty."}


async def signup_social_user(user:dict) -> dict:

    t1_start = process_time()
    # print(data,flush=True)
    # print(type(data),flush=True)
    return_data = dict()

    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_signup',
                            json=user)

        return_data = r.json()
        # print(data,flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return return_data



async def update_user(email:str, user:dict) -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.put(f'{os.getenv("ORM_USER_SERVICE")}/user/email/{email}',
                            json=user)
        data = r.json()
        print(data,flush=True)
    t1_stop = process_time()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start)
    return data


# Retrieve all user
async def read_users(): # -> dict:
    t1_start = process_time()
    data = None
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_USER_SERVICE")}/user/', timeout=300)
        # print(r,flush=True)
        # print(r.json(),flush=True)
        if len(r.json()) > 0:
            data = r.json()
	        
            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start) 
            print("Elapsed time during the whole program in seconds:",
                                                t1_stop-t1_start)     
    return data

# Retrieve all user by matched station ID
async def read_user_by_email(email: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_USER_SERVICE")}/user/email/{email}', timeout=300) 
        print(r.json(),flush=True)
        data = r.json()

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data

# Retrieve all user by matched station ID
async def read_user_by_id(id: str) -> dict:
    t1_start = process_time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{os.getenv("ORM_USER_SERVICE")}/user/id/{id}', timeout=300) 
        # print(r.json(),flush=True)

        data = r.json()['data']

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Retrieve all user by matched station ID
async def read_user_by_social_email(data: dict) -> dict:
    t1_start = process_time()
    # print(data,flush=True)
    # print(type(data),flush=True)
    return_data = dict()

    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/social_email_login',
                            json=data)

        return_data = r.json()
        # print(data,flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return return_data

# Retrieve all user by matched station ID
async def read_user_by_email_password(email: dict)-> dict:
    t1_start = process_time()
    print(email,flush=True)
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/email', json=email) 
        data = r.json() #['data']
        print("read_user_by_email",flush=True)
        print(data,flush=True)

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start) 
        print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start) 
    
    return data


# Delete a user from the database
async def delete_user(email:str):
    r = httpx.delete(f'{os.getenv("ORM_USER_SERVICE")}/user/email/{email}') 
    if r.status_code == 200:
        return True
    return False


async def test_func(request):
    output = {}
    header = dict(request.headers.items())
    print(f'request header       : {header}' )
    output["header"] = header

    param = dict(request.query_params.items())
    print(f'request query params : {param}')  
    output["param"] = param

    try : 
        json = await request.json()
        print(f'request json         : {json}')
        output["json"] = json
    except Exception as err:
        # could not parse json
        body = await request.body()
        print(f'request body         : {body}')
        output["body"]= body
    return output