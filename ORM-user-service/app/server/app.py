import os
import mysql.connector
from time import sleep
from pydantic import BaseModel

from fastapi import FastAPI

from app.server.routes.user import router as UserRouter

def include_router(app):
    app.include_router(UserRouter, tags=["User"], prefix="/user")

def start_application():
    app = FastAPI()
    include_router(app)
    # configure_static(app)
    # create_tables()
    return app


app = start_application()

@app.on_event("startup")
def startup_db_client():
    mysql_flag = False
    mysql_delay = 30

    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_NAME = os.getenv("USER_DATABASE_NAME")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

    cnx = None
    while mysql_flag == False:
        cnx = mysql.connector.connect(user=DATABASE_USERNAME, password=DATABASE_PASSWORD,
                                    host=DATABASE_HOST,
                                    database=DATABASE_NAME)        
        mysql_flag = cnx.is_connected()
        if mysql_flag == False:
            print(f"MongoDB is not Ready yet try again {mysql_delay} seconds later", flush=True)
            sleep(mysql_delay)
    cnx.close()

# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()


@app.get("/", tags=["health_check"])
async def read_root():
    return {"message": "Welcome to health check link"}