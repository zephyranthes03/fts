
async def user_list_to_dict(user_list:list) -> dict:
    print(user_list,flush=True)
    user_dict = dict()
    user_menu_item = ['id','email','create_date','community','phone','email_acceptance','message_acceptance','user_type','expire_time']
    for i in range(len(user_menu_item)):
        user_dict[user_menu_item[i]] = user_list[i]
    return user_dict
