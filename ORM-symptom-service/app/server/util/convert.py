
async def symptom_list_to_dict(symptom_list:list) -> dict:
    print(symptom_list,flush=True)
    symptom_dict = dict()
    symptom_menu_item = ['_id','symptom','area','occur_pattern','ages','sex','bmi','diagnosis','image_file']
    for i in range(len(symptom_menu_item)):
        symptom_dict[symptom_menu_item[i]] = symptom_list[i]
    return symptom_dict

async def disease_list_to_dict(disease_list:list) -> dict:
    print(disease_list,flush=True)
    disease_dict = dict()
    disease_menu_item = ['_id','symptom','area','occur_pattern','ages','sex','diagnosis','image_file']
    for i in range(len(disease_menu_item)):
        disease_dict[disease_menu_item[i]] = disease_list[i]
    return disease_dict

async def sampleimage_list_to_dict(sampleimage_list:list) -> dict:
    print(sampleimage_list,flush=True)
    sampleimage_dict = dict()
    sampleimage_menu_item = ['_id','symptom','area','occur_pattern','ages','sex','bmi','diagnosis','image_file']
    for i in range(len(sampleimage_menu_item)):
        sampleimage_dict[sampleimage_menu_item[i]] = sampleimage_list[i]
    return sampleimage_dict

