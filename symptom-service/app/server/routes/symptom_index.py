import os
import base64

# OpenAI API Key
from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image
# from DeepImageSearch import Load_Data, Search_Setup

from app.server.util.preload import verify_token
from app.server.models.frontend import ApiResponse, PostData

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER", "./symptom/upload/")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER", "./sample/")
    
# templates = Jinja2Templates(directory="templates")

metadata = None 
st = None
from app.server.process.disease import (
    read_diseases,
)

from app.server.process.diagnosis import (
    read_diagnosises,
)


from app.server.process.symptom_index import (
    add_symptom_index,
    delete_symptom_index,
    update_symptom_index,
    read_symptom_index_by_id,
    read_symptom_index_by_name,
    read_symptom_indexes,
    llm_diagnosis,
    llm_diagnosis_base64    
)



from app.server.schemas.symptom_index import (
    ErrorResponseModel,
    ResponseModel,
    Symptom_index_schema,
    Update_symptom_index_schema,
    
)

router = APIRouter()



async def load_symptom_indexes():
    symptom_index_list = Load_Data().from_folder([SAMPLE_IMAGE_FOLDER])

    # Set up the search engine, You can load 'vit_base_patch16_224_in21k', 'resnet50' etc more then 500+ models 
    st = Search_Setup(diagnosis_list=symptom_index_list, model_name='vgg19', pretrained=True, diagnosis_count=20)

    # Index the diagnosises
    st.run_index()

    # Get metadata
    metadata = st.get_diagnosis_metadata_file()



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@router.post("/llm_base64", response_model=ApiResponse, response_description="Upload symptomnostic diagnosis")
async def upload_to_llm_base64(request: Request, data: PostData): #, dependencies:dict=Depends(verify_token)):

    # base64_image = base64.b64encode( symptom_file.file.read()).decode('utf-8')
    query_json = request.json()

    string_bytes = data.base64_image.encode('utf-8')
    base64_bytes = base64.b64encode(string_bytes)
    diseases = await llm_diagnosis_base64(data.base64_image, data.symptom_text, 'dummy@email.com')

    # diseases['llm_content'] = llm_content
    # diseases['symptom'] = extract_symptom(llm_content)
    # diseases['msd'] = extract_msd_link(diseases['symptom'])
    # diseases['query_text'] = query_text
    print("=======", flush=True)
    print(diseases, flush=True)
    llm_result = diseases.get('llm_content', 'error')
    print(diseases.get('llm_content', 'error'), flush=True)

    return ApiResponse(success=True, message=llm_result)
    # return ApiResponse(success=True, message="Test@?")


@router.post("/llm", response_class=HTMLResponse, response_description="Upload symptomnostic diagnosis")
async def upload_to_llm(request: Request, email: str, symptom_text:str, symptom_file: UploadFile = File(...)): #, dependencies:dict=Depends(verify_token)):

    # ext_center = symptom_file.filename[symptom_file.filename.rfind(".")+1:]
    # now = datetime.now()
    # year = now.strftime("%Y")
    # month = now.strftime("%m")
    # date = now.strftime("%d")
    # target_filefolder = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date)

    # if not os.path.exists(target_filefolder):
    #     os.makedirs(target_filefolder)
    # new_center_image = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date, f"{email}_{symptom_file.filename}")

    # write_centor_file = open(new_center_image,'wb')
    # write_centor_file.write(symptom_file.file.read())
    # write_centor_file.close()


    # Path to your image
    # image_path = "/Users/yongjinchong/Downloads/naver/skin/train/건선/스크린샷 2023-07-23 오후 12.03.15.png"

    # Getting the base64 string
    # base64_image = encode_image(symptom_file.file.read())
    # print("symptom_file.file.read()", flush=True)
    # print(symptom_file.file.read())
    base64_image = base64.b64encode( symptom_file.file.read()).decode('utf-8')
    query_json = request.json()

    diseases = await llm_diagnosis(base64_image, symptom_text, email)

    return JSONResponse(status_code=200, content=diseases)


# Request : 서버로 사용자가 증상 발현부를 촬영한 이미지를 서버로 업로드 
# Response : 사용자가 올린 이미지와 비슷한 비교 이미지를 클라이언트로 업로드
@router.post("/request", response_class=HTMLResponse, response_description="Upload symptomnostic diagnosis")
# async def upload_symptom_diagnosis(symptom: Diagnosis_schema = Body(...), file: UploadFile):
# async def upload_symptom(request: Request, email: str, symptom_file: bytes = UploadFile(...)): #, dependencies:dict=Depends(verify_token)):
async def upload_symptom(request: Request, email: str, symptom_center_image: UploadFile = File(...), symptom_wide_image: UploadFile = File(...)): #, dependencies:dict=Depends(verify_token)):

    ## Collecting diagnosis

    ## TODO: Should we Collect diagnosis file type with jpg or png?
    # print(symptom_center_image.filename,flush=True)
    ext_center = symptom_center_image.filename[symptom_center_image.filename.rfind(".")+1:]
    ext_wide = symptom_wide_image.filename[symptom_wide_image.filename.rfind(".")+1:]
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    date = now.strftime("%d")
    target_filefolder = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date)

    if not os.path.exists(target_filefolder):
        os.makedirs(target_filefolder)
    new_center_image = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date, f"{email}_{symptom_center_image.filename}")
    new_wide_image = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date, f"{email}_{symptom_wide_image.filename}")

    write_centor_file = open(new_center_image,'wb')
    write_centor_file.write(symptom_center_image.file.read())
    write_centor_file.close()

    write_wide_file = open(new_wide_image,'wb')
    write_wide_file.write(symptom_wide_image.file.read())
    write_wide_file.close()
        # if st is not None:
        #     symptom_print_list = st.get_similar_diagnosises(diagnosis_path=new_center_image, number_of_diagnosises=9)
        #     print(symptom_print_list,flush=True)

    # return ResponseModel({"status":200, "center_image": new_center_image[new_center_image.rfind('/'):],
    #                       "wide_image": new_wide_image[new_wide_image.rfind('/'):] }, "Uploaded!")
    return JSONResponse(status_code=200, content={"status":200, "center_image": new_center_image[new_center_image.rfind('/'):],
                         "wide_image": new_wide_image[new_wide_image.rfind('/'):] })


# Request : 사용자가 선택한 이미지 리스트를 서버로 전송
# Response : 1. 고객이 한가지 발현증상만 선택한 경우, 바로 증상의 문진 설문조사를 수행
#            2. 고객이 한가지 이상의 발현증상을 선택한 경우, 본인의 증상을 확정할수 있는 추가 프로세스를 수행
@router.post("/request-inspection", response_class=HTMLResponse, response_description="Upload symptomnostic diagnosis")
# async def upload_symptom_diagnosis(symptom: Diagnosis_schema = Body(...), file: UploadFile):
async def request_inspection(request: Request, symptom_id: str, symptom_file_name_list:list): #, dependencies:dict=Depends(verify_token)):
    inspection_dict = {"test1.jpg":{'disease':'desease_1', 'detail':'detail_1', 'queationaire':'queationaire_1'}}

    symptom_file_name_dict = dict()

    for symptom_file_name in symptom_file_name_list:
        if symptom_file_name in symptom_file_name_dict:
            symptom_file_name_dict[symptom_file_name] += 1
        else:
            symptom_file_name_dict[symptom_file_name] = 1

    symptom_file = ""

    if len(symptom_file_name_dict) == 1:
        # return templates.TemplateResponse("request-inspection.html", {"request": request, "disease":diagnosis_dict[image_file_name_list[0]]['disease']})
        # Response : 1. 고객이 한가지 발현증상만 선택한 경우, 바로 증상의 문진 설문조사를 수행
        return ResponseModel({"disease":inspection_dict[symptom_file_name_list[0]]}, "Return disease diagnosis")

    disease_list = list()
    for key,value in symptom_file_name_dict.items():
        disease_list.append(inspection_dict[key])

        # Response : 2. 고객이 한가지 이상의 발현증상을 선택한 경우, 본인의 증상을 확정할수 있는 추가 프로세스를 수행
    return ResponseModel({"diseases":disease_list}, "Return disease diagnosis list")
    # return templates.TemplateResponse("request-inspection_multi.html", {"request":request, "diseases":diseases_list})

# Request : 사용자가 선택한 증상 전달
# Response : 고객이 한가지 발현증상만 선택해서 응답하게 함
@router.post("/request-inspection-help", response_class=HTMLResponse, response_description="Upload symptomnostic disease")
# async def upload_symptom_diagnosis(symptom: Diagnosis_schema = Body(...), file: UploadFile):
async def request_inspection(request: Request, symptom_id: str, symptom_file_name:str, dependencies:dict=Depends(verify_token)):
    inspection_dict = {"test1.jpg":{'disease':'desease_1', 'detail':'detail_1', 'queationaire':'queationaire_1'}}

    return ResponseModel({"disease":inspection_dict[symptom_file_name]}, "Return disease diagnosis")



@router.post("/", response_description="Symptom_index data folder added into the database")
async def add_Symptom_index_data(symptom_index: Symptom_index_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    symptom_index = jsonable_encoder(symptom_index)
    new_symptom_index = await add_symptom_index(symptom_index)
    if new_symptom_index.get('error', None):
        return ErrorResponseModel(
            new_symptom_index.get('error', None),
            500,
            new_symptom_index.get('message', None)
        )
    
    return ResponseModel(new_symptom_index, "Symptom_index added successfully.")


@router.get("/", response_description="symptomnostics retrieved")
async def get_symptom_indexes(): #dependencies:dict=Depends(verify_token)):
    symptom_indexes = await read_symptom_indexes()
    if symptom_indexes:
        return ResponseModel(symptom_indexes, "Symptoms data statistic retrieved successfully")
    return ResponseModel(symptom_indexes, "Empty list returned")

@router.get("/id/{id}", response_description="Symptoms retrieved")
async def get_symptom_by_id(id:str): #, dependencies:dict=Depends(verify_token)):
    symptom_indexes = await read_symptom_index_by_id(id)
    if symptom_indexes:
        return ResponseModel(symptom_indexes, "Symptoms data statistic retrieved successfully")
    return ResponseModel(symptom_indexes, "Empty list returned")

@router.get("/name/{name}", response_description="Symptoms retrieved")
async def get_symptom_by_name(name:str): #, dependencies:dict=Depends(verify_token)):
    symptom_indexes = await read_symptom_index_by_name(name)
    if symptom_indexes:
        return ResponseModel(symptom_indexes, "Symptoms data statistic retrieved successfully")
    return ResponseModel(symptom_indexes, "Empty list returned")

@router.put("/id/{id}")
async def update_symptom_index_data(id: str, req: Update_symptom_index_schema = Body(...)): #, dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    symptom = jsonable_encoder(req)
    updated_symptom_index = await update_symptom_index(id, symptom)
    if 'data' in updated_symptom_index:
        return ResponseModel(
            "Symptom_index with ID: {} name update is successful".format(id),
            "Symptom_index name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the symptom_index data.",
    )

@router.delete("/id/{id}", response_description="Symptom_index data deleted from the database")
async def delete_symptom_index_data(id:str): #, dependencies:dict=Depends(verify_token)):
    deleted_symptom_index = await delete_symptom_index(id)
    if deleted_symptom_index == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )