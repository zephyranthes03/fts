
extract_symptom_dict = {
    "아토피":"아토피", 
    "발진":"발진", 
    "알러지":"알레르기", 
    "알레르기":"알레르기",
    "내성발톱":"내성발톱", 
    "백선":"백선",
    "혈종":"혈종",
    "진균증":"진균증",
    "링웜":"링웜"
}

extract_disease_dict = {
    "아토피":"아토피", 
    "발진":"발진", 
    "알러지":"알레르기", 
    "알레르기":"알레르기",
    "내성발톱":"내성발톱", 
    "백선":"백선",
    "혈종":"혈종",
    "진균증":"진균증",
    "링웜":"링웜"
}

def extract_symptom(llm_content:str):
    return_item_list = list()
    for extract_str,extract_item in extract_symptom_dict.items():
        if extract_str in llm_content:
            return_item_list.append(extract_item)
    return return_item_list

def extract_disease(llm_content:str):
    return_item_list = list()
    for extract_str,extract_item in extract_disease_dict.items():    
        if extract_str in llm_content:
            return_item_list.append(extract_item)
    return return_item_list