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
from app.server.util.logging import logger

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER")
SAMPLE_IMAGE_FOLDER = os.getenv("SAMPLE_IMAGE_FOLDER")

# templates = Jinja2Templates(directory="templates")

metadata = None 
st = None

from app.server.process.post import (
    read_post_by_id,
    like_post_by_id,
    read_post_by_name,
    read_posts,
    add_post,
    delete_post,
    update_post,
)

from app.server.schemas.post import (
    ErrorResponseModel,
    ResponseModel,
    Post_schema,
    Update_post_schema
)


router = APIRouter()

UPLOAD_IMAGE_FOLDER = os.getenv("UPLOAD_IMAGE_FOLDER", "./board/upload/")



@router.post("/{community_id}/{board_id}", response_description="Post data folder added into the database")
async def add_post_data(community_id:str, board_id:str, post: Post_schema = Body(...), dependencies:dict=Depends(verify_token)):
    post = jsonable_encoder(post)
    new_post = await add_post(community_id, board_id, post)
    if new_post.get('error', None):
        return ErrorResponseModel(
            new_post.get('error', None),
            500,
            new_post.get('message', None)
        )
    return ResponseModel(new_post, "Post added successfully.")

@router.get("/{community_id}/{board_id}", response_description="Posting thread on the community")
async def get_posts(community_id:str, board_id:str, dependencies:dict=Depends(verify_token)):
    posts = await read_posts(community_id, board_id)
    if posts:
        return ResponseModel(posts, "Communities data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.get("/{community_id}/{board_id}/read/{id}", response_description="Communities post retrieved")
async def get_post_by_id(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    posts = await read_post_by_id(community_id, board_id, id)
    if posts:
        return ResponseModel(posts, "Communities data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.get("/{community_id}/{board_id}/like/{id}", response_description="Communities retrieved")
async def get_post_by_id(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    logger.info(dependencies)
    posts = await like_post_by_id(community_id, board_id, id, dependencies)
    if posts:
        return ResponseModel(posts, "Communities data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")


@router.get("/{community_id}/{board_id}/name/{name}", response_description="Communities retrieved")
async def get_post_by_name(community_id:str, board_id:str, name:str, dependencies:dict=Depends(verify_token)):
    posts = await read_post_by_name(community_id, board_id, name)
    if posts:
        return ResponseModel(posts, "Communities data statistic retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.put("/{community_id}/{board_id}/id/{id}")
async def update_post_data(community_id:str, board_id:str, id: str, req: Update_post_schema = Body(...), dependencies:dict=Depends(verify_token)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    logger.info(req)
    post = jsonable_encoder(req)
    updated_post = await update_post(community_id, board_id, id, post)
    if 'data' in updated_post:
        return ResponseModel(
            "Post with ID: {} name update is successful".format(id),
            "Post name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the post data.",
    )

@router.delete("/{community_id}/{board_id}/id/{id}", response_description="Post data deleted from the database")
async def delete_post_data(community_id:str, board_id:str, id:str, dependencies:dict=Depends(verify_token)):
    deleted_post = await delete_post(community_id, board_id, id)
    if deleted_post == True:
        return ResponseModel(id, " record is Deleted")
    return ErrorResponseModel(
        "An error occurred", 404, "Database deletation is failiure"
    )


# Request : 서버로 사용자가 증상 발현부를 촬영한 이미지를 서버로 업로드 
# Response : 사용자가 올린 이미지와 비슷한 비교 이미지를 클라이언트로 업로드
@router.post("/request", response_class=HTMLResponse, response_description="Upload image for post content")
# async def upload_symptom_diagnosis(symptom: Diagnosis_schema = Body(...), file: UploadFile):
# async def upload_symptom(request: Request, email: str, symptom_file: bytes = UploadFile(...)): #, dependencies:dict=Depends(verify_token)):
async def upload_symptom(request: Request, email: str, image: UploadFile = File(...)): #, dependencies:dict=Depends(verify_token)):

    ## Collecting diagnosis

    ## TODO: Should we Collect diagnosis file type with jpg or png?
    # logger.info(image.filename)
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