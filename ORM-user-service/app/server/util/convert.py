import ast
async def user_list_to_dict(user_list:list) -> dict:
    user_dict = dict()

    user_menu_item = ['email','create_date','community','phone','email_acceptance','message_acceptance',
                      'user_type','expire_time','last_check_time','interested_tag','message','friend','permission']

    eval_user_menu_item = ['community','message_acceptance','last_check_time',
                           'interested_tag','friend','permission']

    for i in range(len(user_menu_item)):
        if user_menu_item[i] in eval_user_menu_item:
            user_dict[user_menu_item[i]] = ast.literal_eval(user_list[i])
        else:
            user_dict[user_menu_item[i]] = user_list[i]

    # print(user_dict,flush=True)
    return user_dict
