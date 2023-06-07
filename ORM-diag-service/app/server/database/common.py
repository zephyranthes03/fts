import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/diag'
DATABASE_HOST = os.getenv("DATABASE_HOST")
DIAG_DATABASE_NAME = os.getenv("DIAG_DATABASE_NAME")
DIAG_DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DIAG_TABLENAME = "diag"
DISEASE_TABLENAME = "disease"
IMAGE_TABLENAME = "SAMPLEIMAGE"


# SQLAlchemy specific code, as with any other app
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)


class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance

class Inital_database(SingletonClass):
    engine = sqlalchemy.create_engine(
            url="mysql+mysqldb://{0}:{1}@{2}/{3}".format(
                DIAG_DATABASE_USERNAME, DATABASE_PASSWORD_UPDATED, DATABASE_HOST, DIAG_DATABASE_NAME
                )
            )

    metadata = sqlalchemy.MetaData()

    diags = sqlalchemy.Table(
        DIAG_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("disease", sqlalchemy.String(45)),
        sqlalchemy.Column("image_file", sqlalchemy.String(255)),
        sqlalchemy.Column("detail", sqlalchemy.Text),
        sqlalchemy.Column("queationaire", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    diseases = sqlalchemy.Table(
        DISEASE_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("disease", sqlalchemy.String(255)),
        sqlalchemy.Column("detail", sqlalchemy.Text),
        sqlalchemy.Column("queationaire", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    sampleimages = sqlalchemy.Table(
        IMAGE_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("image_file", sqlalchemy.String(255)),
        sqlalchemy.Column("detail", sqlalchemy.Text),
        sqlalchemy.Column("inspection", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    metadata.create_all(engine)

database = Inital_database()

class Diag(BaseModel):
    __tablename__ = DIAG_TABLENAME
    id: str
    disease: str
    image_file: str
    detail: str
    queationaire: str
    # create_date: datetime


class Disease(BaseModel):
    __tablename__ = DISEASE_TABLENAME
    id: str
    disease: str
    detail: str
    queationaire: str
    # create_date: datetime


class SampleImage(BaseModel):
    __tablename__ = IMAGE_TABLENAME
    id: str
    image_file: str
    detail: str
    inspection: str
    # create_date: datetime