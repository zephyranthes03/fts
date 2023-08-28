import os
from pathlib import Path

class Settings:
    DATABASE_MEMBER: str  = os.getenv("COMMUNITY_DATABASE_MEMBER", "member")
    DATABASE_APPLICATION: str  = os.getenv("COMMUNITY_DATABASE_APPLICATION", "application")

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