import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image
from DeepImageSearch import Load_Data, Search_Setup

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

templates = Jinja2Templates(directory="templates")

metadata = None 
st = None
from app.server.process.disease import (
    read_diseases,
)

from app.server.process.image import (
    read_images,
)


from app.server.process.diag import (
    add_image,
    delete_image,
    update_image,
    read_image_by_id,
    read_images
)



from app.server.models.diag import (
    ErrorResponseModel,
    ResponseModel,
    SampleImageSchema,
    UpdateSampleImageModel,
)

router = APIRouter()

async def load_images():
    image_list = Load_Data().from_folder([SAMPLE_IMAGE_FOLDER])

    # Set up the search engine, You can load 'vit_base_patch16_224_in21k', 'resnet50' etc more then 500+ models 
    st = Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=20)

    # Index the images
    st.run_index()

    # Get metadata
    metadata = st.get_image_metadata_file()


# Request : 서버로 사용자가 증상 발현부를 촬영한 이미지를 서버로 업로드 
# Response : 사용자가 올린 이미지와 비슷한 비교 이미지를 클라이언트로 업로드
@router.post("/request", response_class=HTMLResponse, response_description="Upload diagnostic image")
# async def upload_diag_image(diag: SampleImageSchema = Body(...), file: UploadFile):
async def upload_diag_image(request: Request, diag_id: str, image_file: bytes = File(...)):

    ## Collecting image

    ## TODO: Should we Collect image file type with jpg or png?
    ext = image_file.filename[image_file.rfind(".")+1:]
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    date = now.strftime("%d")
    target_filefolder = os.path.join(UPLOAD_IMAGE_FOLDER, year, month)
    if os.path.exists(target_filefolder):
        os.makedirs(target_filefolder)
    new_filename = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date, f"{diag_id}.{ext}")

    with open(image_file.filename,'rb') as file:
        write_file = open(new_filename,'wb')
        write_file.write(await file.read())
        write_file.close()
        if st is not None:
            image_print_list = st.get_similar_images(image_path=new_filename, number_of_images=9)
            print(image_print_list)

    # return templates.TemplateResponse("select_disease_sample.html", {"request": request, "image_list":image_print_list})
    return ResponseModel({"similiar_image_list":image_print_list}, "Return Similar image")


# Request : 사용자가 선택한 이미지 리스트를 서버로 전송
# Response : 1. 고객이 한가지 발현증상만 선택한 경우, 바로 증상의 문진 설문조사를 수행
#            2. 고객이 한가지 이상의 발현증상을 선택한 경우, 본인의 증상을 확정할수 있는 추가 프로세스를 수행
@router.post("/request-inspection", response_class=HTMLResponse, response_description="Upload diagnostic image")
# async def upload_diag_image(diag: SampleImageSchema = Body(...), file: UploadFile):
async def request_inspection(request: Request, diag_id: str, image_file_name_list:list):
    inspection_dict = {"test1.jpg":{'disease':'desease_1', 'detail':'detail_1', 'queationaire':'queationaire_1'}}

    image_file_name_dict = dict()

    for image_file_name in image_file_name_list:
        if image_file_name in image_file_name_dict:
            image_file_name_dict[image_file_name] += 1
        else:
            image_file_name_dict[image_file_name] = 1

    image_file = ""

    if len(image_file_name_dict) == 1:
        # return templates.TemplateResponse("request-inspection.html", {"request": request, "disease":image_dict[image_file_name_list[0]]['disease']})
        # Response : 1. 고객이 한가지 발현증상만 선택한 경우, 바로 증상의 문진 설문조사를 수행
        return ResponseModel({"disease":inspection_dict[image_file_name_list[0]]}, "Return disease image")

    disease_list = list()
    for key,value in image_file_name_dict.items():
        disease_list.append(inspection_dict[key])

        # Response : 2. 고객이 한가지 이상의 발현증상을 선택한 경우, 본인의 증상을 확정할수 있는 추가 프로세스를 수행
    return ResponseModel({"diseases":disease_list}, "Return disease image list")
    # return templates.TemplateResponse("request-inspection_multi.html", {"request":request, "diseases":diseases_list})

# Request : 사용자가 선택한 증상 전달
# Response : 고객이 한가지 발현증상만 선택해서 응답하게 함
@router.post("/request-inspection-help", response_class=HTMLResponse, response_description="Upload diagnostic disease")
# async def upload_diag_image(diag: ImageSchema = Body(...), file: UploadFile):
async def request_inspection(request: Request, diag_id: str, image_file_name:str):
    inspection_dict = {"test1.jpg":{'disease':'desease_1', 'detail':'detail_1', 'queationaire':'queationaire_1'}}

    return ResponseModel({"disease":inspection_dict[image_file_name]}, "Return disease image")


@router.get("/", response_description="diagnostics retrieved")
async def get_diags():
    diags = await read_diags()
    if diags:
        return ResponseModel(diags, "Diags data statistic retrieved successfully")
    return ResponseModel(diags, "Empty list returned")

@router.get("/{id}", response_description="Diags retrieved")
async def get_diag(id:str):
    diags = await read_diag_by_id(id)
    if diags:
        return ResponseModel(diags, "Diags data statistic retrieved successfully")
    return ResponseModel(diags, "Empty list returned")

@router.put("/{id}")
async def update_diag_data(id: str, req: UpdateSampleImageModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    diag = jsonable_encoder(req)
    updated_diag = await update_diag(id, diag)
    if 'data' in updated_diag:
        return ResponseModel(
            "Diag with ID: {} name update is successful".format(id),
            "Diag name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the diag data.",
    )

@router.delete("/{id}", response_description="Diag data deleted from the database")
async def delete_diag_data(id:str):
    deleted_diag = await delete_diag(id)
    if deleted_diag == True:
        return ResponseModel([], "Database is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )