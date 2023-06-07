
async def diag_list_to_dict(diag_list:list) -> dict:
    print(diag_list,flush=True)
    diag_dict = dict()
    diag_menu_item = ['id','disease','image_file','detail','queationaire']
    for i in range(len(diag_menu_item)):
        diag_dict[diag_menu_item[i]] = diag_list[i]
    return diag_dict

async def disease_list_to_dict(disease_list:list) -> dict:
    print(disease_list,flush=True)
    disease_dict = dict()
    disease_menu_item = ['id','disease','detail','queationaire']
    for i in range(len(disease_menu_item)):
        disease_dict[disease_menu_item[i]] = disease_list[i]
    return disease_dict

async def sampleimage_list_to_dict(sampleimage_list:list) -> dict:
    print(sampleimage_list,flush=True)
    sampleimage_dict = dict()
    sampleimage_menu_item = ['id','image_file','detail','inspection']
    for i in range(len(sampleimage_menu_item)):
        sampleimage_dict[sampleimage_menu_item[i]] = sampleimage_list[i]
    return sampleimage_dict

