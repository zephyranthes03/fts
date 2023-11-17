import redis
import json
import os
from app.config.redis_config import redis_config
from app.server.util.encrypt import generate_password_hash

async def session_load(session_key:str) -> dict:
	rd = redis_config()
	json_str = rd.get(session_key)
	if json_str is not None:
		return json.loads(json_str)
	return {}

async def session_update(session_key:str, session_dict:dict) -> dict:
	rd = redis_config()
	session_str = json.dumps(session_dict)
	rd.set(session_key, session_str)

async def session_delete(session_key:str):
	rd = redis_config()
	rd.delete(session_key)
	return session_key

async def session_create(session_dict:dict) -> str:
	rd = redis_config()
	if os.getenv("SESSION_SALT") is not None:
		if 'email' in session_dict:
			print("session_dict",flush=True)
	# 		print(session_dict,flush=True)
	# 		print(session_dict['email'],flush=True)
	# 		email = str(await generate_password_hash(session_dict['email']))
	# 		session_dict["id"] = email
	# 		session_str = json.dumps(session_dict)
	# 		rd.set(email, session_str)
	# 		rd.expire(email, session_dict["expire_time"] * 60)
	# 		return session_dict
	# 	else:
	# 		return {'error': "email couldn't found"}
	# else:
	# 	return {'error': 'Session salt not defined'}
