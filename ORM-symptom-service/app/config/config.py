import os
from pathlib import Path

class Settings:

    SYMPTOM_TABLENAME = "symptom"
    DISEASE_TABLENAME = "disease"
    IMAGE_TABLENAME = "sampleimage"

    SYMPTOM_DATABASE_NAME: str = os.getenv("SYMPTOM_DATABASE_NAME", "symptom")
    MONGO_INITDB_ROOT_USERNAME: str = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_INITDB_ROOT_PASSWORD: str = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DATABASE_URI = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGODB_URL}"
    # DATABASE_URI = f"mongodb://{MONGODB_URL}" # mongodb+srv://<username>:<password>@sandbox.jadwj.mongodb.net
    # SECRET_KEY: str = os.getenv("SECRET_KEY")
    # ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins

    TEST_USER_EMAIL = "test@example.com"

settings = Settings()