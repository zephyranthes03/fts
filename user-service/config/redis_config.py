# config/redis_config.py
from datetime import timedelta
import os
from random import random
from dotenv import load_dotenv

load_dotenv()

def redis_config() :
	
    try:
        redisURL="redis://localhost:6379/1", #os.getenv("REDIS_HOST")
        sessionIdName="sessionId",
        sessionIdGenerator=lambda: str(random.randint(1000, 9999)),
        expireTime=timedelta(days=1),
		
    except:
        print("redis connection failure")
