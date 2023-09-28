import os
from pathlib import Path

class Settings:

    SYMPTOM_TABLENAME = "symptom"
    DISEASE_TABLENAME = "disease"
    IMAGE_TABLENAME = "diagnosis"

    TEST_USER_EMAIL = "test@example.com"

    UPLOAD_IMAGE_FOLDER = "./upload/"
    SAMPLE_IMAGE_FOLDER = "./sample/"

settings = Settings()