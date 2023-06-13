
from fastapi import FastAPI, Header, HTTPException
from app.server.util.session import session_load

async def verify_token(session_key: str = Header(None)):
    if session_key is None:
        raise HTTPException(status_code=400, detail="Invalid session")
    else:
        session = session_load(session_key)
    return session