import ast

from datetime import datetime
from app.server.models.user import UserSchema, SocialEmailSignupSchema

async def user_from_str(user_list:list) -> dict:
    user_list.pop(1) # remove password field

    user_dict = dict()
    

    user_menu_item = ['email','create_date','community','phone','email_acceptance','message_acceptance',
                      'user_type','account_type','expire_time','last_check_time','interested_tag','message',
                      'friend','permission','symptom_id','symptom_tag','username','nickname','age','gender']

    eval_user_menu_item = ['community','message_acceptance','account_type','last_check_time',
                           'interested_tag','friend','permission','symptom_id','symptom_tag']

    for i in range(len(user_menu_item)):
        if user_menu_item[i] in eval_user_menu_item:
            user_dict[user_menu_item[i]] = ast.literal_eval(user_list[i])
        else:
            user_dict[user_menu_item[i]] = user_list[i]

    # print(user_dict,flush=True)
    return user_dict

async def user_to_str(user_dict:dict) -> dict:

    eval_user_menu_item = ['community','message_acceptance','account_type','last_check_time',
                           'interested_tag','friend','permission','symptom_id','symptom_tag']

    for key,value in user_dict.items():
        if key in eval_user_menu_item:
            user_dict[key] = str(value)
        else:
            user_dict[key] = value

    # print(user_dict,flush=True)
    return user_dict

 
async def social_user_to_userSchema(user:SocialEmailSignupSchema) -> UserSchema:
    now = datetime.utcnow()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    userSchema = UserSchema(
        email = user['email'],
        password = "empty_password_for_the_social_user",
        create_date = formatted_now,
        community = {},
        phone = "",
        email_acceptance = "",
        message_acceptance = [],
        user_type = "user",
        account_type = [user['login_type']],
        expire_time = 30,
        last_check_time = {},
        interested_tag = [],
        message = False,
        friend = [],
        permission = {
            "survey": False
        },
        symptom_id = [],
        symptom_tag = [],
        username = user['extra_data']['username'],
        nickname = user['extra_data']['nickname'],
        age = user['extra_data']['age'],
        gender = user['extra_data']['gender']
    )
    return userSchema


    #     user_temp['account_type'].append(user['login_type']) if user['login_type'] not in user_temp['account_type'] else None


    # t1_start = process_time()
    
    # async with httpx.AsyncClient() as client:

    #     user_temp = {
    #     "email": "john_doe1@gmail.com",
    #     "password": "j8s7f98pupaoihefiudy78t2rq3gsfd",
    #     "create_date": "2021-01-01 00:00:00",
    #     "community": {
    #         "acne": {
    #         "grade": "user",
    #         "status": "early"
    #         }
    #     },
    #     "phone": "72065122567",
    #     "email_acceptance": "all",
    #     "message_acceptance": [
    #         "community",
    #         "system"
    #     ],
    #     "user_type": "user",
    #     "account_type": [
    #         "email"
    #     ],
    #     "expire_time": 30,
    #     "last_check_time": {
    #         "community_id": "2021-01-01T00:00:00Z"
    #     },
    #     "interested_tag": [
    #         "tag1",
    #         "tag2"
    #     ],
    #     "message": False,
    #     "friend": [],
    #     "permission": {
    #         "survey": "open"
    #     },
    #     "symptom_id": [],
    #     "symptom_tag": [],
    #     "username": "John Doe",
    #     "nickname": "John11",
    #     "age": "40-49",
    #     "gender": "M"
    #     }

    #     user_temp['email'] = user['email']
    #     user_temp['account_type'].append(user['login_type']) if user['login_type'] not in user_temp['account_type'] else None
    #     user_temp['username'] = user['extra_data']['username']
    #     user_temp['nickname'] = user['extra_data']['nickname']
    #     user_temp['gender'] = user['extra_data']['gender']
    #     user_temp['age'] = user['extra_data']['age']

    #     # print(user_temp,flush=True)
    #     email = user_temp.get('email', None)
    #     if email:
    #         r = await client.get(f'{os.getenv("ORM_USER_SERVICE")}/user/email/{email}')
    #         data = r.json() 
    #         # print(data,flush=True)
    #         # print(data.get("email",None),flush=True)
    #         if data.get("email", None) is None:
    #             print(f'{os.getenv("ORM_USER_SERVICE")}/user/',flush=True)
    #             r = await client.post(f'{os.getenv("ORM_USER_SERVICE")}/user/', json=user_temp)
    #             data = r.json() 
    #             t1_stop = process_time()
    #             print("Elapsed time:", t1_stop, t1_start) 
    #             print("Elapsed time during the whole program in seconds:",
    #                                                 t1_stop-t1_start)
    #             return {'email':user_temp.get('email')}

    #         else:
    #             return {"error": "Email already exist!"}

    #     else:
    #         return {"error": "Email couldn't be Empty."}
    
