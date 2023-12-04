
extract_list = {
    "아토피", 
    "발진", 
    "알러지", 
    "알레르기",
    "내성발톱", 
    "백선",
    "혈종",
    "진균증",
    "링웜"
}
def extract_symptom(llm_content:str):
    return_list = list()
    for extract_str in extract_list:
        if extract_str in llm_content:
            return_list.append(extract_str)
    return return_list