# config/redis_config.py
from datetime import timedelta
import os
import redis
from random import random
from dotenv import load_dotenv

load_dotenv()

def redis_config():
    try:
        REDIS_HOST = str = os.getenv("REDIS_HOST")
        REDIS_PORT = integer = os.getenv("REDIS_PORT")
        REDIS_DATABASE = integer = os.getenv("REDIS_DATABASE")
        rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE) 
        return rd       		
    except:
        print("Redis connection failure")
