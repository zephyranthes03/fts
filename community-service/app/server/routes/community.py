import os

from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile, Request, Depends

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

# from fastapi.templating import Jinja2Templates

from io import BytesIO
from PIL import Image

from app.server.util.preload import verify_token

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

# templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.community import (
    read_community_by_id,
    read_community_by_name,
    read_communities,
    add_community,
    delete_community,
    update_community
)

from app.server.schemas.community import (
    ErrorResponseModel,
    ResponseModel,
    Community_schema,
    Update_community_schema
)


router = APIRouter()

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER", "./community/upload/")


@router.post("/", response_description="Community data folder added into the database")
async def add_community_data(community: Community_schema = Body(...), dependencies:dict=Depends(verify_token)):
    community = jsonable_encoder(community)
    new_community = await add_community(community)
    if new_community.get('error', None):
        return ErrorResponseModel(
            new_community.get('error', None),
            500,
            new_community.get('message', None)
        )
    return ResponseModel(new_community, "Community added successfully.")


@router.get("/", response_description="Communities retrieved")
async def get_communities(dependencies:dict=Depends(verify_token)):
    communities = await read_communities()
    if communities:
        return ResponseModel(communities, "Communities data statistic retrieved successfully")
    return ResponseModel(communities, "Empty list returned")

@router.get("/id/{id}", response_description="Communities retrieved")
async def get_community_by_id(id:str, dependencies:dict=Depends(verify_token)):
    communities = await read_community_by_id(id)
    if communities:
        return ResponseModel(communities, "Communities data statistic retrieved successfully")
    return ResponseModel(communities, "Empty list returned")

@router.get("/name/{name}", response_description="Communities retrieved")
async def get_community_by_name(name:str, dependencies:dict=Depends(verify_token)):
    communities = await read_community_by_name(name)
    if communities:
        return ResponseModel(communities, "Communities data statistic retrieved successfully")
    return ResponseModel(communities, "Empty list returned")

@router.put("/id/{id}")
async def update_community_data(id: str, req: Update_community_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req,flush=True)
    community = jsonable_encoder(req)
    updated_community = await update_community(id, community)
    if 'data' in updated_community:
        return ResponseModel(
            "Community with ID: {} name update is successful".format(id),
            "Community name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the community data.",
    )

@router.delete("/id/{id}", response_description="Community data deleted from the database")
async def delete_community_data(id:str, dependencies:dict=Depends(verify_token)):
    deleted_community = await delete_community(id)
    if deleted_community == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )



# Request : 서버로 사용자가 증상 발현부를 촬영한 이미지를 서버로 업로드 
# Response : 사용자가 올린 이미지와 비슷한 비교 이미지를 클라이언트로 업로드
@router.post("/request", response_class=HTMLResponse, response_description="Upload image for community")
# async def upload_symptom_diagnosis(symptom: Diagnosis_schema = Body(...), file: UploadFile):
# async def upload_symptom(request: Request, email: str, symptom_file: bytes = UploadFile(...)): #, dependencies:dict=Depends(verify_token)):
async def upload_symptom(request: Request, email: str, image: UploadFile = File(...)): #, dependencies:dict=Depends(verify_token)):

    ## Collecting diagnosis

    ## TODO: Should we Collect diagnosis file type with jpg or png?
    # print(image.filename,flush=True)
    ext_center = image.filename[image.filename.rfind(".")+1:]
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    date = now.strftime("%d")
    target_filefolder = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date)

    if not os.path.exists(target_filefolder):
        os.makedirs(target_filefolder)
    uplaoded_image = os.path.join(UPLOAD_IMAGE_FOLDER, year, month, date, f"{email}_{image.filename}")

    write_centor_file = open(uplaoded_image,'wb')
    write_centor_file.write(image.file.read())
    write_centor_file.close()

    # return ResponseModel({"status":200, "center_image": new_center_image[new_center_image.rfind('/'):],
    #                       "wide_image": new_wide_image[new_wide_image.rfind('/'):] }, "Uploaded!")
    return JSONResponse(status_code=200, content={"status":200, "uploaded_image": uplaoded_image[uplaoded_image.rfind('/'):] })