import redis
import json
import os
from app.config.redis_config import redis_config

async def session_load(session_key:str) -> dict:
	rd = redis_config()
	json_str = rd.get(session_key)
	if json_str is not None:
		return json.loads(json_str)
	return {}

