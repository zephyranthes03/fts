import ast
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
            print
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
