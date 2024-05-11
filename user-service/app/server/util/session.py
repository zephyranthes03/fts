import redis
import json
import os
from app.config.redis_config import redis_config
from app.server.util.encrypt import generate_password_hash
from app.server.util.logging import logger

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
			logger.info("session_dict")
			logger.info(session_dict)
			logger.info(session_dict['email'])
			email = session_dict['email'] # str(await generate_password_hash(session_dict['email']))
			session_dict_out = dict()
			session_dict_out["id"] = email
			session_dict_out["login_type"] = session_dict["login_type"]
			session_dict_out["access_token"] = session_dict["access_token"]
			session_dict_out["refresh_token"] = session_dict["refresh_token"]
			session_dict_out["expire_time"] = session_dict["expire_time"]

			session_str = json.dumps(session_dict_out)
			rd.set(email, str(session_dict_out))
			rd.expire(email, session_dict_out["expire_time"] * 60)
			return session_dict_out
		else:
			return {'error': "email couldn't found"}
	else:
		return {'error': 'Session salt not defined'}
