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
from app.server.models.frontend import ApiResponse, PostData, PutData
from app.server.util.logging import logger

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


from app.server.process.llm_result import (
    llm_diagnosis,
    llm_diagnosis_base64,
    read_llm_feedbacks,
    update_llm_feedbacks,
    delete_llm_result
)

from app.server.schemas.symptom_index import (
    ErrorResponseModel,
    ResponseModel,
    Symptom_index_schema,
    Update_symptom_index_schema,
    
)

router = APIRouter()



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


@router.post("/llm_base64", response_model=ApiResponse, response_description="Upload symptomnostic diagnosis")
async def upload_to_llm_base64(request: Request, data: PostData): #, dependencies:dict=Depends(verify_token)):

    query_json = await request.json()
    diseases = await llm_diagnosis_base64(data.base64_image, data.symptom_text, 'dummy@email.com')

    return diseases

@router.put("/llm_base64/{id}", response_model=ApiResponse, response_description="Upload symptomnostic diagnosis")
async def upload_feedback_to_llm_base64(id:str, request: Request, data: PutData): #, dependencies:dict=Depends(verify_token)):

    query_json = await request.json()
    diseases = await update_llm_feedbacks(id, data)

    # diseases['llm_content'] = llm_content
    # diseases['symptom'] = extract_symptom(llm_content)
    # diseases['msd'] = extract_msd_link(diseases['symptom'])
    # diseases['query_text'] = query_text
    logger.info("=======", )
    logger.info(diseases, )
    message_content = diseases.get('message_content', 'error')
    feedback = diseases.get('feedback', 2)
    status = True if message_content != 'error' else False

    # return JSONResponse(status_code=200, content=diseases)

    return ApiResponse(success=status, message=feedback, message_content=message_content,id=id)
    # return ApiResponse(success=True, message="Test@?")

@router.post("/llm", response_class=JSONResponse, response_description="Upload symptomnostic diagnosis")
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
    # logger.info("symptom_file.file.read()", )
    # logger.info(symptom_file.file.read())
    base64_image = base64.b64encode( symptom_file.file.read()).decode('utf-8')
    query_json = request.json()

    diseases = await llm_diagnosis(base64_image, symptom_text, email)

    return JSONResponse(status_code=200, content=diseases)



@router.get("/feedback/{type}", response_description="llm feedback retrieved")
async def get_llm_feedback(type:str): #dependencies:dict=Depends(verify_token)):
    llm_feedbacks = await read_llm_feedbacks(type)
    if llm_feedbacks:
        return ResponseModel(llm_feedbacks, "Feedback data statistic retrieved successfully")
    return ResponseModel(llm_feedbacks, "Empty list returned")

@router.delete("/{id}", response_description="Symptom_index data deleted from the database")
async def delete_symptom_index_data(id:str): #, dependencies:dict=Depends(verify_token)):
    deleted_symptom_index = await delete_llm_result(id)
    if deleted_symptom_index == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )