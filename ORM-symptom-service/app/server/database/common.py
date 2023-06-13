import sqlalchemy
import urllib
import os

from datetime import datetime

from typing import List

# import databases
# from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#DATABASE_URL = 'mysql+mysqldb://root:default@mysql/symptom'
DATABASE_HOST = os.getenv("DATABASE_HOST")
SYMPTOM_DATABASE_NAME = os.getenv("SYMPTOM_DATABASE_NAME")
SYMPTOM_DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

SYMPTOM_TABLENAME = "symptom"
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
                SYMPTOM_DATABASE_USERNAME, DATABASE_PASSWORD_UPDATED, DATABASE_HOST, SYMPTOM_DATABASE_NAME
                )
            )

    metadata = sqlalchemy.MetaData()

    symptoms = sqlalchemy.Table(
        SYMPTOM_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("symptom", sqlalchemy.String(1024)),
        sqlalchemy.Column("area", sqlalchemy.String(1024)),
        sqlalchemy.Column("occur_pattern", sqlalchemy.String(1024)),
        sqlalchemy.Column("ages", sqlalchemy.String(255)),
        sqlalchemy.Column("sex", sqlalchemy.String(16)),
        sqlalchemy.Column("bmi", sqlalchemy.Float),
        sqlalchemy.Column("diagnosis", sqlalchemy.String(255)),
        sqlalchemy.Column("queationaire", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    diseases = sqlalchemy.Table(
        DISEASE_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("symptom", sqlalchemy.String(1024)),
        sqlalchemy.Column("area", sqlalchemy.String(1024)),
        sqlalchemy.Column("occur_pattern", sqlalchemy.String(1024)),
        sqlalchemy.Column("ages", sqlalchemy.String(255)),
        sqlalchemy.Column("sex", sqlalchemy.String(16)),
        sqlalchemy.Column("diagnosis", sqlalchemy.String(255)),
        sqlalchemy.Column("queationaire", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    sampleimages = sqlalchemy.Table(
        IMAGE_TABLENAME,
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
        sqlalchemy.Column("symptom", sqlalchemy.String(1024)),
        sqlalchemy.Column("area", sqlalchemy.String(1024)),
        sqlalchemy.Column("occur_pattern", sqlalchemy.String(1024)),
        sqlalchemy.Column("ages", sqlalchemy.String(255)),
        sqlalchemy.Column("sex", sqlalchemy.String(16)),
        sqlalchemy.Column("bmi", sqlalchemy.Float),
        sqlalchemy.Column("diagnosis", sqlalchemy.String(255)),
        sqlalchemy.Column("queationaire", sqlalchemy.Text),
        # sqlalchemy.Column("create_date", sqlalchemy.Date),
    )

    metadata.create_all(engine)

database = Inital_database()

class Symptom(BaseModel):
    __tablename__ = SYMPTOM_TABLENAME
    id: str
    symptom: str
    area: str
    occur_pattern: str
    ages: str
    sex: str
    bmi: float
    diagnosis: str
    image_file: str
    # create_date: datetime


class Disease(BaseModel):
    __tablename__ = DISEASE_TABLENAME
    id: str
    symptom: str
    area: str
    occur_pattern: str
    ages: str
    sex: str
    diagnosis: str
    image_file: str
    # create_date: datetime


class SampleImage(BaseModel):
    __tablename__ = IMAGE_TABLENAME
    id: str
    symptom: str
    area: str
    occur_pattern: str
    ages: str
    sex: str
    bmi: float
    diagnosis: str
    image_file: str
    # create_date: datetime